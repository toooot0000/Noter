import enum
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_cors import CORS

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/todoList'
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(myApp)
migrate = Migrate(myApp, db)

CORS(myApp)

timeFmt = "%Y-%m-%dT%H:%M"


class todoSates(enum.Enum):
    undue = 0
    completed = 1
    overdue = 2
    deleted = 3
    unstarted = 4


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    content = db.Column(db.String(100))
    urgency = db.Column(db.Integer)
    state = db.Column(db.Enum(todoSates), default=0)


@myApp.route("/add", methods=["POST"])
def addTodo():
    print(request.json)
    # start, end = YYYY-MM-DDTHH:MM
    # %Y-%m-%dT%H:%M
    start = datetime.strptime(request.json['start'], timeFmt)
    end = datetime.strptime(request.json['end'], timeFmt)
    content = request.json['title']
    urgency = request.json['urgency']
    state = todoSates.undue
    newTodo = Todo(state=state, start=start, end=end,
                   content=content, urgency=urgency)
    db.session.add(newTodo)
    db.session.commit()
    return "Recieved!"


@myApp.route("/get")
def getTodos():
    print('Request to get!')
    allTodos = None
    # 查询全部
    if request.args.get('all'):
        print('Request to get all!')
        allTodos = Todo.query.filter(
            Todo.state != todoSates.completed, Todo.state != todoSates.deleted).all()
        # print(allTodos)
    # 按照页数查询
    elif request.args.get('page'):
        page = int(request.args.get('page'))
        perPage = int(request.args.get('perPage')) if request.args.get(
            'perPage') else 5
        print("Request to get page %d, per page %d" % (page, perPage))
        allTodos = Todo.query.filter(
            Todo.state != todoSates.completed, Todo.state != todoSates.deleted).paginate(page=page, per_page=perPage, error_out=False).items
    # 按照ID查询
    elif request.args.get('todoId'):
        todoId = int(request.args.get('todoId'))
        allTodos = Todo.query.filter(Todo.id == todoId).all()
    if allTodos:
        res = {}
        for todo in allTodos:
            res[todo.id] = {
                'id': todo.id,
                'start': todo.start.strftime(timeFmt),
                'end': todo.end.strftime(timeFmt),
                'title': todo.content,
                'urgency': todo.urgency,
                'state': todo.state.name,
            }
        return jsonify(res)
    return "Wrong data!"


@myApp.route("/getAvailId")
def getAvailId():
    from sqlalchemy.sql import func
    print(request)
    return jsonify({"availId": db.session.query(func.max(Todo.id)).scalar()+1})


@myApp.route("/complete")
def complete():
    if not request.args.get('todoId'):
        return make_response('No Such id', 404)
    update(request.args.get('todoId'), 'state', todoSates.completed)
    return "Success!"


@myApp.route("/delete")
def delete():
    if not request.args.get('todoId'):
        return make_response('No Such id', 404)
    update(request.args.get('todoId'), 'state', todoSates.deleted)
    return "Success!"


@myApp.route('/update')
def updateTodo():
    if not request.args.get('todoId'):
        return make_response('No Such id', 404)
    update(request.args.get('todoId'), 'state', todoSates.overdue)
    return "Success!"


# * 用来处理提交的修改


@myApp.route('/submit', methods=["POST"])
def submitList():
    print(request.json)
    for id in request.json.keys():
        change = request.json[id]
        res = Todo.query.filter(Todo.id == int(id)).scalar()
        if res:  # 该ID已存在
            for key in change.keys():
                val = change[key]
                if key == "title":
                    setattr(res, "content", change[key])
                elif key == "state":
                    setattr(res, key, todoSates[val])
                elif key == "start" or key == "end":
                    setattr(res, key, datetime.strptime(val, timeFmt))
                elif key == "urgency":
                    setattr(res, key, int(val))
    db.session.commit()
    return "Fail"


def update(id, propName, value):
    todo = Todo.query.get(id)
    setattr(todo, propName, value)
    db.session.commit()
    pass
