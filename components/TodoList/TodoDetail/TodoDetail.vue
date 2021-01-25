<template>
  <view class="wrapper" :class="{ hidden: isHidden }">
    <MovableCard
      :height="200"
      :left="left"
      :right="right"
      :stopMove="stopMove"
      @move-left="completeTodo"
      @move-right="deleteTodo"
    >
      <template v-slot:back-msg-left>
        <view class="back-msg-wrapper">
          <view class="back-msg right">完 成</view>
        </view>
      </template>
      <template v-slot:back-msg-right>
        <view class="back-msg-wrapper">
          <view class="back-msg left">删 除</view>
        </view>
      </template>
      <template v-slot:content>
        <view class="card-container" :animation="cardAnimData">
          <view class="card">
            <view class="upper">
              <view class="icon-ctn">
                <view
                  class="icon"
                  :style="{ 'background-color': iconColor }"
                ></view>
              </view>
              <view class="content">
                <view class="title">{{ todo.title }}</view>
                <view class="subtitle">{{
                  todo.end.date + " " + todo.end.time
                }}</view>
              </view>
            </view>
            <view class="seperater"></view>
            <view class="lower">
              <view class="content">
                <view class="progress-ctn">
                  <progress
                    :percent="100 - remain.percent"
                    stroke-width="6"
                    activeColor="#BDBDBD"
                    :active="true"
                    active-mode="forwards"
                    :backgroundColor="iconColor"
                    class="progress"
                  />
                </view>
                <view class="remain-info"
                  >剩余：{{ remain.percent + "%" }}</view
                >
              </view>
            </view>
          </view>
        </view>
      </template>
    </MovableCard>
  </view>
</template>

<script>
import MovableCard from "components/TodoList/MovableCard/MovableCard";

export default {
  name: "TodoDetail",
  components: {
    MovableCard,
  },
  props: {
    todo: {
      type: Object,
      default: function () {
        return {
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
        };
      },
    },
    startColor: {
      type: String,
      default: "#ADFF2F",
    },
    endColor: {
      type: String,
      default: "#FF6347",
    },
  },
  data: () => ({
    remain: {
      d: 0,
      h: 0,
      m: 0,
      t: 0,
      percent: 20,
    },
    left: {
      color: "#1e92e0",
      event: "move-left",
    },
    right: {
      color: "#e77e7e",
      event: "move-right",
    },
    iconColor: "#FFF",
    interval: null,
    hasEmited: false,
    stopMove: false,
    cardAnimData: null,
    isHidden: false,
  }),
  mounted() {
    this.todo.start.parsed = this.parseDate(this.todo.start);
    this.todo.end.parsed = this.parseDate(this.todo.end);
    this.updateRemain();
    this.updateColor();
    this.interval = setInterval(() => {
      this.updateRemain();
      this.updateColor();
    }, 1000);
    this.hasEmited = false;
  },
  methods: {
    gradientColors(ratio) {
      // convert #hex notation to rgb array
      let parseColor = function (hexStr) {
        return hexStr.length === 4
          ? hexStr
              .substr(1)
              .split("")
              .map(function (s) {
                return 0x11 * parseInt(s, 16);
              })
          : [hexStr.substr(1, 2), hexStr.substr(3, 2), hexStr.substr(5, 2)].map(
              function (s) {
                return parseInt(s, 16);
              }
            );
      };

      // zero-pad 1 digit to 2
      let pad = function (s) {
        return s.length === 1 ? "0" + s : s;
      };

      let gradientColors = function (start, end, ratio, gamma = 1) {
        let i,
          j,
          ms,
          me,
          output = [],
          so = [];
        let normalize = function (channel) {
          return Math.pow(channel / 255, gamma);
        };
        start = parseColor(start).map(normalize);
        end = parseColor(end).map(normalize);
        // for (i = 0; i < steps; i++) {
        //     ms = i / (steps - 1);
        //     me = 1 - ms;
        //     for (j = 0; j < 3; j++) {
        //         so[j] = pad(Math.round(Math.pow(start[j] * me + end[j] * ms, 1 / gamma) * 255).toString(16));
        //     }
        //     output.push('#' + so.join(''));
        // }
        for (j = 0; j < 3; j++) {
          so[j] = pad(
            Math.round(
              Math.pow(start[j] * (1 - ratio) + end[j] * ratio, 1 / gamma) * 255
            ).toString(16)
          );
        }
        return "#" + so.join("");
      };
      return gradientColors(this.startColor, this.endColor, ratio);
    },
    completeTodo() {
      if (!this.hasEmited) {
        // console.log('完成！')
        this.hasEmited = true;
        this.stopMove = true;
        // this.todo.state = 'complete'

        this.cardSlideAnim(1000, () => {
          // console.log('完成！')
          this.todo.state = "completed";
          this.$emit("complete-todo", this.todo.id);
        });
      }
    },
    deleteTodo() {
      if (!this.hasEmited) {
        // console.log('删除！')
        this.hasEmited = true;
        this.stopMove = true;
        // this.todo.state = 'deleted'
        this.cardSlideAnim(-1000, () => {
          // console.log(this)
          this.todo.state = "deleted";
          this.$emit("delete-todo", this.todo.id);
        });
      }
    },
    updateColor() {
      this.iconColor = this.gradientColors((100 - this.remain.percent) / 100);
      // console.log(this.iconColor)
    },
    updateRemain() {
      let now = new Date();
      this.remain.t =
        this.todo.end.parsed - now < 0 ? 0 : this.todo.end.parsed - now;
      let totalTime = this.todo.end.parsed - this.todo.start.parsed;
      // console.log("Total time: " + totalTime);
      // console.log("Remain percent: " + this.remain.t / totalTime);
      this.remain.percent = Math.ceil(
        100 * (this.remain.t / totalTime < 1 ? this.remain.t / totalTime : 1)
      );
      // TODO:
      // * 1. 当时间的时候，计算剩余天数、小时数、分钟数
      // * 2. 动态判断是否过期，如果过期则emit update-todo(todoId)，将该todo的状态更改为overdue
      // // 3. 将时间统一为北京时间
    },
    parseDate(obj) {
      let date = obj.date.split("-");
      let y = parseInt(date[0]);
      let m = parseInt(date[1]) - 1;
      let d = parseInt(date[2]);
      let time = obj.time.split(":");
      let h = parseInt(time[0]);
      let mm = parseInt(time[1]);
      return new Date(y, m, d, h, mm, 0);
    },
    cardSlideAnim(dis, handler) {
      let anim = uni.createAnimation({
        duration: 100,
        timingFunction: "ease-out",
      });
      anim.translateX(dis).step();
      this.cardAnimData = anim.export();
      setTimeout(() => {
        this.cardAnimData = null;
        this.isHidden = true;
        setTimeout(() => {
          handler();
        }, 200);
      }, 101);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/static/sass/projConfig.scss";
.wrapper {
  margin: 40rpx 0rpx;
  box-sizing: border-box;
  transition: all;
  transition-duration: 0.2s;
}

.hidden {
  opacity: 0;
}

.card-container {
  background-color: white;
  width: 95%;
  height: 100%;
  margin: 0 auto; // border: 1px solid black;
  box-shadow: 0 3rpx 10rpx rgba(0, 0, 0, 0.2);
}

.back-msg-wrapper {
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  justify-content: center;
  color: white;
  padding: 0 20rpx;
}

.back-msg {
  font-size: 40px;
}

.seperater {
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(189, 189, 189, 0),
    #d0d0d0 5%,
    #d0d0d0 50%,
    #d0d0d0 95%,
    rgba(189, 189, 189, 0)
  );
  margin: 15rpx auto;
}

.card {
  padding: 0 30rpx;
  height: 100%;
  display: flex;
  flex-flow: column nowrap;
  align-items: start;
  .upper {
    margin-top: 20rpx;
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    .icon-ctn {
      display: inline-block;
      height: 100%;
      display: flex;
      flex-flow: column nowrap;
      justify-content: center;
      .icon {
        width: 60rpx;
        height: 60rpx;
        background-color: black;
      }
    }
    .content {
      margin-left: 20rpx;
      display: inline-block;
    }
  }
  .content {
    display: inline-block;
    .title {
      font-size: $fnt-size-title;
    }
    .subtitle {
      font-size: $fnt-size-subtitle;
    }
  }
  .lower {
    width: 100%;
    .content {
      width: 100%;
      .progress-ctn {
        margin: 5rpx auto;
        width: 100%;
      }
      .progress {
        width: 100%;
      }
      .remain-info {
        font-size: $fnt-size-content;
      }
    }
  }
}
</style>
