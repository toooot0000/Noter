<script>
export default {
	onLaunch: function() {
		console.log('App Launch')
	},
	onShow: function() {
		console.log('App Show')
	},
	onHide: function() {
		console.log('App Hide')
	},
	globalData: {
		urgencyLevel: ["不急", "有点急", "很急", "不完成能死"],
	},
}
</script>

<style lang="scss">
/*每个页面公共css */
@import url("./static/css/base.css");

page {
  width: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background: rgba(241, 241, 241, 0.25);
  font-family: sans-serif;
}
</style>
