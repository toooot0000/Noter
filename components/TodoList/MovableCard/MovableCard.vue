<template>
  <view class="wrapper" :key="key">
    <view class="back-part" :style="{'background-color':backColor,'text-align':backAlign}">
      <view class="back-msg-l" :class="{'collapse':isLeft}">
        <slot name="back-msg-left"></slot>
      </view>
      <view class="back-msg-r" :class="{'collapse':isRight}">
        <slot name="back-msg-right"></slot>
      </view>
    </view>
    <movable-area :style="{'height': height + 'rpx'}">
      <movable-view
        direction="horizontal"
        :x="x"
        @change="onChange"
        :out-of-bounds="false"
        :damping="100"
      >
        <slot name="content">占位信息</slot>
      </movable-view>
    </movable-area>
  </view>
</template>
// TODO:
// 1. 屏幕改变大小的时候改变滑动初始位置
<script>
export default {
    name: "MovableCard",
    data() {
        return {
            scnWidth: 0,
            threshold: 40,

            x: 100,
            xInit: 100,
            xMax: 100,
            old: {
                x: 0,
            },
            timer: null,
            isMoving: false,
            isLeft: true,
            isRight: true,
            isLeftLimit: false,
            isRightLimit: false,

            backColor: "rgba(0, 0, 0, 0)",
            backAlign: "left",
            backMsg: "信息！",
            backMsgCtnStyle: {

            },
            backMsgStyle: {
                color: "rgba(0, 0, 0, 0)"
            },
            key: "myKey",

            animData:{
                // 用于传递动画信息
            }
        }
    },
    props: {
        height: {
            type: Number,
            default: 100
        },
        left: {
            type: Object,
            default: () => {
                return {
                    color: "#00ff00",
                    event: "move-left"
                }
            },
        },
        right: {
            type: Object,
            default: () => {
                return {
                    color: "#ff0000",
                    event: "move-right"
                }
            },
        },
        stopMove:{
            type: Boolean,
            default: false,
        }
    },
    beforeMount: function() {
        let that = this;
        uni.getSystemInfo({
            success: function(res) {
                that.scnWidth = res.windowWidth;
            }
        })
        this.x = this.scnWidth;
        this.xInit = this.x;
        this.xMax = this.scnWidth * 2.0;
        uni.onWindowResize(this.onWindowResize)
        
    },
    destroyed() {
        uni.offWindowResize(this.onWindowResize)
    },
    methods: {
        onWindowResize({ size: { windowWidth, windowHeight } }){
            // console.log('Resize!')
            this.srnWidth = windowWidth
            this.x = this.scnWidth;
            this.xInit = this.x;
            this.xMax = this.scnWidth * 2.0;
        },
        onChange(e) {
            // 检查拖动状态
            this.isMoving = true;
            clearTimeout(this.timer);
            this.timer = setTimeout(() => {
                this.isMoving = false
            }, 200)

            this.old.x = e.detail.x;

            let xx = e.detail.x;

            // 判断滑动位置
            if (xx < this.threshold && !this.isLeftLimit) {
                // console.log('滑到左边！')
                this.isLeftLimit = true;
                this.emitMoveEvent(this.right.event)
            } else if (xx > this.threshold && this.isLeftLimit) {
                this.isLeftLimit = false;
            } else if (xx > this.xMax - this.threshold && !this.isRightLimit) {
                // console.log('滑到右边！')
                this.isRightLimit = true;
                this.emitMoveEvent(this.left.event)
            } else if (xx < this.xMax - this.threshold && this.isRightLimit) {
                this.isRightLimit = false;
            }
            // 如果 x<initX 说明往左滑的，底色改绿
            // 如果 x>initX 说明往左滑的，底色改红
            let ratio = Math.abs((xx - this.xInit) / (this.xMax)) * 2; // 理论上在0-1
            let toRGBA = function(sColor, a) {
                sColor = sColor.toLowerCase();
                //十六进制颜色值的正则表达式
                let reg = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/;
                // 如果是16进制颜色
                if (sColor && reg.test(sColor)) {
                    if (sColor.length === 4) {
                        let sColorNew = "#";
                        for (let i = 1; i < 4; i += 1) {
                            sColorNew += sColor.slice(i, i + 1).concat(sColor.slice(i, i + 1));
                        }
                        sColor = sColorNew;
                    }
                    //处理六位的颜色值
                    let sColorChange = [];
                    for (let i = 1; i < 7; i += 2) {
                        sColorChange.push(parseInt("0x" + sColor.slice(i, i + 2)));
                    }
                    return "RGBA(" + sColorChange.join(",") + "," + a + ")";
                }
                return sColor;
            }
            let target = null;
            this.isLeft = true;
            this.isRight = true;
            if (xx < this.xInit) {
                this.backAlign = "right";
                target = this.right;
                this.isLeft = true;
                this.isRight = false;
            } else if (xx > this.xInit) {
                this.backAlign = "left";
                target = this.left;
                this.isLeft = false;
                this.isRight = true;

            }
            if (target !== null) {
                this.backColor = toRGBA(target.color, ratio);

            }

        },
        emitMoveEvent(event) {
            let that = this;
            let obj = {
                detail: {
                    x: that.x,
                },
                key: this.key,
            };
            this.$emit(event, obj)
        }
    },
    watch: {
        isMoving: function(n, o) {
            if (n) {
                // console.log("在动！")
            } else if (!this.stopMove) {
                // console.log("不在动！")
                this.x = this.old.x;
                this.$nextTick(function() {
                    this.x = this.xInit;
                })
            }
        }
    }
}
</script>

<style lang="scss">
$areaWidth: 300%;
.collapse {
  visibility: hidden;
  display: none;
}

.wrapper {
  position: relative;
  overflow: visible;
}

movable-area {
  position: relative;
  left: -($areaWidth - 100%)/2;
  width: $areaWidth;
}

movable-view {
  height: 100%;
  width: 100% / $areaWidth * 100%;
}

.back-part {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: gold;
}

.back-msg {
  color: white;
  height: 100%;
  &-l,
  &-r {
    height: 100%;
  }
}
</style>