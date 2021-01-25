<template>
  <view class="content">
    <view class="f-ctn-row f-jst-cen">
      <view class="title">TO DO LIST!!!</view>
    </view>

    <InputBox @input-todo="onInputTodo"></InputBox>

    <TodoList
      :todoList="todoList"
      @complete-todo="completeTodo"
      @delete-todo="deleteTodo"
      @update-todo="updateTodo"
    ></TodoList>
  </view>
</template>




<script>
// todo 滑动加载
// todo 根据紧急度调整前面的icon颜色
// todo 前端判断是否overdue，超过时间后向页面提交修改

import MovableCard from "components/TodoList/MovableCard/MovableCard";
import InputBox from "components/InputBox/InputBox";
import TodoList from "components/TodoList/TodoList";
export default {
  components: {
    InputBox,
    MovableCard,
    TodoList,
  },
  data() {
    return {
      title: "Hello",
      testMsg: "",
      todoList: [],
      page: 1,
      perPage: 3,
      changes: {},
      currentId: 0,
    };
  },
  onLoad() {
    let that = this;
    that.refreshList();
    // 获取当前最大可用ID数
    that.commonRequest({
      url: "getAvailId",
      success(data) {
        // console.log(data);
        that.currentId = data.data.availId;
      },
    });
    // 设置数据同步;
    setInterval(() => {
      that.submitChange();
    }, 30000);
  },
  destroyed() {
    this.submitChange();
  },
  methods: {
    onInputTodo(todo) {
      Date.prototype.Format = function (fmt) {
        //author: meizz
        var o = {
          "M+": this.getMonth() + 1, //月份
          "d+": this.getDate(), //日
          "h+": this.getHours(), //小时
          "m+": this.getMinutes(), //分
          "s+": this.getSeconds(), //秒
          "q+": Math.floor((this.getMonth() + 3) / 3), //季度
          S: this.getMilliseconds(), //毫秒
        };
        if (/(y+)/.test(fmt))
          fmt = fmt.replace(
            RegExp.$1,
            (this.getFullYear() + "").substr(4 - RegExp.$1.length)
          );
        for (var k in o)
          if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(
              RegExp.$1,
              RegExp.$1.length == 1
                ? o[k]
                : ("00" + o[k]).substr(("" + o[k]).length)
            );
        return fmt;
      };
      todo.start =
        new Date().Format("yyyy-MM-dd") + "T" + new Date().Format("hh:mm");
      // console.log(todo.start);
      todo.end = todo.date + "T" + todo.time;
      // console.log(todo);
      this.addTodo(todo);
    },
    sendTodo(todo) {
      // ! 添加todo必须向服务器同步
      let that = this;
      that.commonRequest({
        url: "add",
        method: "POST",
        data: todo,
        success: () => {
          console.log("成功收到！");
        },
      });
    },
    addTodo(todo) {
      // ! 为了保证添加的id和前端维护的id相同，添加一条todo就必须给后端发送一条
      let that = this;
      todo.id = that.currentId;
      // that.changes[that.currentId] = {
      //   ...todo,
      // };
      that.sendTodo(todo);
      that.todoList.push(this.processTodo(todo));
      that.currentId++;
    },
    getTodo(options, handler) {
      /// 从服务区获取todo信息的
      /// options.all/page/id
      let that = this;
      let _options = {
        url: "get",
        success: handler,
      };
      if ("all" in options && options.all === true) {
        _options.data = {
          all: true,
        };
      } else if ("page" in options && typeof options.page === "number") {
        _options.data = {
          page: parseInt(options.page),
          perPage:
            "perPage" in options && typeof options.perPage === "number"
              ? parseInt(options.perPage)
              : 5,
        };
      } else if ("id" in options && typeof options.id === "number") {
        _options.data = {
          todoId: parseInt(options.id),
        };
      }
      this.commonRequest(_options);
    },
    completeTodo(id) {
      this.updateTodo(id, {
        props: "state",
        value: "completed",
      });
    },
    deleteTodo(id) {
      this.updateTodo(id, {
        props: "state",
        value: "deleted",
      });
    },
    updateTodo(
      id,
      change = {
        props: "state",
        value: "undue",
      }
    ) {
      let _change = this.changes[id];
      if (typeof _change != "object") {
        _change = {};
        this.changes[id] = _change;
      }
      _change[change.props] = change.value;
      console.log("更新列表！");
      this.submitChange();
    },
    refreshList(type = "page") {
      this.todoList = [];
      let that = this;
      this.getTodo(
        {
          all: type === "all" ? true : undefined,
          page: type === "page" ? that.page : undefined,
          perPage: type === "page" ? that.perPage : undefined,
        },
        (data) => {
          data = data.data;
          // console.log(data);
          if (typeof data == "object") {
            for (let item in data) {
              this.todoList.push(this.processTodo(data[item]));
            }
          }
        }
      );
    },
    processTodo(raw) {
      let item = {
        ...raw,
      };
      // console.log(data[item])
      let start = item.start.split("T");
      item.start = {};
      item.start.date = start[0];
      item.start.time = start[1];
      let end = item.end.split("T");
      item.end = {};
      item.end.date = end[0];
      item.end.time = end[1];
      return item;
    },
    commonRequest(
      options = {
        url: "",
        data: {},
        method: "GET",
        success: ({ data, statusCode, header }) => {},
        fail: (error) => {
          console.log(error);
        },
      }
    ) {
      uni.request({
        url: "http://127.0.0.1:5000/" + options.url,
        data: options.data || {},
        header: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
        method: options.method || "GET",
        dataType: "json",
        sslVerify: true,
        success: options.success || (({ data, statusCode, header }) => {}),
        fail:
          options.fail ||
          ((error) => {
            console.log(error);
          }),
      });
    },
    submitChange() {
      console.log("提交修改！");
      let that = this;
      if (Object.keys(this.changes).length > 0) {
        that.commonRequest({
          url: "submit",
          method: "POST",
          data: that.changes,
          success: () => {
            console.log("提交修改成功！好耶！");
            that.changes = {};
          },
          fail: (e) => {
            console.log("呜呜呜没有提交成功");
          },
        });
      }
    },
  },
};
</script>

<style scoped>
.title {
  color: black;
  font-size: 35px;
  margin-top: 35rpx;
  margin-bottom: 20rpx;
}
</style>
