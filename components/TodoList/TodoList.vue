<template>
  <view class="todo-list wrapper">
    <transition-group tag="view" name="todo-cards">
      <view v-for="todo in todoList" :key="todo.id">
        <TodoDetail
          class="todo-detail"
          v-if="todo.state !== 'completed' && todo.state !== 'deleted'"
          :todo="todo"
          :key="todo.id"
          @complete-todo="completeTodo"
          @delete-todo="deleteTodo"
          @update-todo="updateTodo"
        ></TodoDetail>
      </view>
    </transition-group>
  </view>
</template>

<script>
// v-if="todo.state !== 'completed' && todo.state !== 'deleted'"
import TodoDetail from "components/TodoList/TodoDetail/TodoDetail";
export default {
  props: {
    todoList: {
      type: Array,
      default: () => [
        {
          id: 0,
          title: "我要做！",
          urgency: 0,
          end: {
            date: "2090-01-01",
            time: "00:00",
            parsed: null,
          },
          start: {
            date: "1990-01-01",
            time: "00:00",
            parsed: null,
          },
          state: "undue",
        },
        {
          id: 1,
          title: "我不要要做！",
          urgency: 0,
          end: {
            date: "2023-01-01",
            time: "00:00",
            parsed: null,
          },
          start: {
            date: "2001-01-01",
            time: "00:00",
            parsed: null,
          },
          state: "undue",
        },
      ],
    },
  },
  data: () => ({}),
  components: {
    TodoDetail,
  },
  // mounted(){
  //   console.log(this.todoList)
  // },
  methods: {
    completeTodo(todoId) {
      console.log("完成了：" + todoId);
      this.$emit("complete-todo", todoId);
    },
    deleteTodo(todoId) {
      console.log("删掉了：" + todoId);
      this.$emit("delete-todo", todoId);
    },
    updateTodo(todo) {
      console.log("更改了：" + todo);
      this.$emit("update-todo", todo);
    },
  },
};
</script>
<style lang="scss" scoped>
.todo-list {
  position: relative;
  padding-top: 30rpx;
  padding-bottom: 30rpx;
}

.todo-cards-leave-to,
.todo-cards-enter {
  opacity: 0;
  transition: all 0.5s;
}

.todo-cards-enter-active {
  transition: all 0.5s;
  transform: translateX(-100%);
}

.todo-cards-move {
  transition: all 0.5s;
}

.todo-cards-leave-active {
  position: absolute;
  transition: all 0.5s;
}

.todo-detail {
  transition: all 1s;
}
</style>
