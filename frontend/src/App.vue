<script>
import userStore from './store/user.js'

export default {
  onLaunch: function () {
    // 启动时恢复登录态
    userStore.init()
  },
}
</script>

<style>
/* 全局公共样式 */
page {
  background-color: #f5f6fa;
  font-size: 28rpx;
  color: #333;
  -webkit-font-smoothing: antialiased;
}

/* 通用卡片 */
.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin: 20rpx 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

/* 主按钮 */
.btn-primary {
  background: linear-gradient(135deg, #ff6b35, #ff4d4f);
  color: #fff;
  border-radius: 48rpx;
  font-size: 32rpx;
  font-weight: 600;
  text-align: center;
  padding: 22rpx 0;
  border: none;
}

.btn-primary::after {
  border: none;
}

/* 空状态 */
.empty-box {
  padding: 120rpx 0;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}

/* 价格文本 */
.price {
  color: #ff4d4f;
  font-weight: 700;
}

/* 安全区底部条 */
.safe-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
