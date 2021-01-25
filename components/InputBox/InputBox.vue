<template>
  <view class="wrapper">
    <view class="container f-ctn-row f-jst-l f-wrp-w">
      <view class="lable">内容</view>
      <input
        type="text"
        v-model="title"
        class="title"
        placeholder="你要干啥？"
        label="你要干啥？"
      />
    </view>
    <view class="container f-ctn-row f-jst-l f-wrp-w">
      <view class="date">
        <view class="lable">目标日期</view>
        <picker :value="date" @change="onDateChanged" mode="date">
          <view class="uni-input">{{ date }}</view>
        </picker>
      </view>
    </view>
    <view class="container f-ctn-row f-jst-l f-wrp-w">
      <view class="time">
        <view class="lable">目标时间</view>
        <picker :value="time" @change="onTimeChanged" mode="time">
          <view class="uni-input">{{ time }}</view>
        </picker>
      </view>
    </view>
    <view class="container f-ctn-row f-jst-l f-wrp-w">
      <view class="lable">紧急度</view>
      <picker :range="urgency" :value="index" @change="onUrgencyChanged">
        <view class="uni-input">{{ urgency[index] }}</view>
      </picker>
    </view>
    <view class="container f-ctn-row f-jst-cen f-wrp-nw">
      <button class="btn submit" hover-class="btn-hover" @click="onSubmit">
        OJBK
      </button>
      <button class="btn clear" hover-class="btn-hover" @click="onClear">
        NOJBK
      </button>
    </view>
  </view>
</template>


<script>
export default {
  name: "InputBox",
  data: () => {
    return {
      title: "",
      urgency: [],
      index: 0,
      date: "1990-01-01",
      time: "00:00",
    };
  },
  beforeMount() {
    this.refresh();
  },
  methods: {
    refresh() {
      let that = this;
      that.title = "";
      that.index = 0;
      let d = new Date();
      let checkDig = (v) => {
        return v < 10 ? "0" + v : "" + v;
      };
      that.date = `${d.getFullYear()}-${checkDig(d.getMonth() + 1)}-${checkDig(
        d.getDate()
      )}`;
      that.time = `${checkDig(d.getHours())}:${checkDig(d.getMinutes())}`;
      that.urgency = getApp().globalData.urgencyLevel;
    },
    onUrgencyChanged(e) {
      let that = this;
      that.index = e.detail.value;
    },
    log(msg) {
      console.log(msg);
    },
    onDateChanged(e) {
      let that = this;
      that.date = e.detail.value;
    },
    onTimeChanged(e) {
      let that = this;
      that.time = e.detail.value;
    },
    onSubmit(e) {
      let that = this;
      // 做个校验，看下ddl时间是不是比现在要远
      let ddl = new Date(that.date + "T" + that.time);
      let now = new Date();
      //   console.log(ddl);
      if (ddl.getTime() < now.getTime()) {
        uni.showToast({
          title: "长者警告！",
          icon: "none",
          mask: true,
        });
      } else if (that.title) {
        uni.showToast({
          title: "成功添加！",
          icon: "success",
          mask: true,
        });
        let todo = {
          title: that.title,
          time: that.time,
          date: that.date,
          urgency: that.index,
        };
        that.$emit("input-todo", todo);
        that.refresh();
      } else {
        uni.showToast({
          title: "总得干点啥吧！",
          icon: "none",
          mask: true,
        });
      }
    },
    onClear(e) {
      this.refresh();
      uni.showToast({
        title: "清空内容",
        icon: "none",
        mask: true,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
$cnt-bd-color: rgba(211, 211, 211, 0.26);
$label-text-color: #838383;
$content-text-color: #464646;
$text-font-size: 18px;
$btn-submit-color: #1e92e0;
$btn-clear-color: #e77e7e;

.container {
  width: 100%;
  background-color: white;
  border-top: 1rpx solid $cnt-bd-color;
  border-bottom: 1rpx solid $cnt-bd-color;
  margin: 17rpx 0;
  padding: 5rpx 15rpx;
}

.lable,
picker,
input {
  display: inline-block;
  font-size: $text-font-size;
  color: $content-text-color;
}

.lable {
  width: 200rpx;
  font-size: $text-font-size;
  color: $label-text-color;
}

.btn {
  background-color: rgba(241, 241, 241, 0.5);
  width: 30%;
  transition-property: all;
  transition-duration: 0.3s;
  color: white;
  text-align: center;
  cursor: pointer;
  border: 0;
  border-radius: 2rpx;
}

.btn.submit {
  background-color: $btn-submit-color;
}

.btn.clear {
  background-color: $btn-clear-color;
}

// .btn-hover {
//   background-color: rgba(241, 241, 241, 0.8);
// }

.btn-hover.submit {
  background-color: #1f5a81;
}

.btn-hover.clear {
  background-color: #b83c3c;
}
</style>