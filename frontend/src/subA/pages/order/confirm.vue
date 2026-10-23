<template>
  <view class="page">
    <!-- 订单信息 -->
    <view class="card">
      <view class="order-title">{{ eventTitle }}</view>
      <view class="order-row">
        <text class="label">场次</text>
        <text class="value">{{ sessionName }}（{{ formatTime(startTime) }}）</text>
      </view>
      <view class="order-row">
        <text class="label">票档</text>
        <text class="value">{{ ticketName }} ¥{{ ticketPrice }}</text>
      </view>
      <view class="order-row">
        <text class="label">数量</text>
        <text class="value">{{ qty }} 张</text>
      </view>
      <view class="order-row">
        <text class="label">场馆</text>
        <text class="value">{{ venue }}（{{ city }}）</text>
      </view>
      <view class="order-row">
        <text class="label">合计</text>
        <text class="value price">¥{{ amount }}</text>
      </view>
    </view>

    <!-- 备注 -->
    <view class="card">
      <view class="section-title">备注</view>
      <textarea
        v-model="remark"
        class="remark-input"
        placeholder="选填，如有特殊需求请备注（如连座等）"
        maxlength="200"
      />
    </view>

    <!-- 底部结算 -->
    <view class="bottom-bar safe-bottom">
      <view class="bottom-price">
        <text class="label">合计</text>
        <text class="price">¥{{ amount }}</text>
      </view>
      <view class="submit-btn" :class="{ disabled: submitting }" @click="submitOrder">
        {{ submitting ? '提交中...' : '提交订单' }}
      </view>
    </view>
  </view>
</template>

<script>
import { api } from '../../../api/index.js'

export default {
  data() {
    return {
      sessionId: null,
      ticketTypeId: null,
      qty: 1,
      amount: '0.00',
      remark: '',
      eventTitle: '',
      sessionName: '',
      startTime: '',
      ticketName: '',
      ticketPrice: '0',
      venue: '',
      city: '',
      submitting: false,
    }
  },
  onLoad(options) {
    this.sessionId = Number(options.session_id)
    this.ticketTypeId = Number(options.ticket_type_id)
    this.qty = Number(options.qty || 1)
    this.amount = options.amount || '0.00'
    this.eventTitle = this.safeDecode(options.event_title)
    this.sessionName = this.safeDecode(options.session_name)
    this.startTime = this.safeDecode(options.start_time)
    this.ticketName = this.safeDecode(options.ticket_name)
    this.ticketPrice = options.ticket_price || '0'
    this.venue = this.safeDecode(options.venue)
    this.city = this.safeDecode(options.city)
  },
  methods: {
    // 兼容：H5（双重编码 %25xx）与小程序（单层编码 %xx / 原始中文）
    safeDecode(v) {
      if (!v) return ''
      let s = String(v)
      for (let i = 0; i < 2; i++) {
        try {
          const d = decodeURIComponent(s)
          if (d === s) break
          s = d
        } catch (e) {
          break
        }
      }
      return s
    },
    formatTime(t) {
      const s = this.safeDecode(t)
      return s.replace('T', ' ').slice(0, 16)
    },
    submitOrder() {
      if (this.submitting) return
      if (!this.$user.isLogin) {
        uni.showToast({ title: '请先登录', icon: 'none' })
        setTimeout(() => uni.navigateTo({ url: '/pages/login/login' }), 600)
        return
      }
      this.submitting = true
      api
        .createOrder({
          session_id: this.sessionId,
          ticket_type_id: this.ticketTypeId,
          quantity: this.qty,
          remark: this.remark,
        })
        .then((res) => {
          const order = res.data
          uni.showModal({
            title: '下单成功',
            content: `订单号：${order.order_no}\n应付金额：¥${order.amount}（模拟支付）`,
            confirmText: '立即支付',
            cancelText: '稍后支付',
            success: (r) => {
              if (r.confirm) {
                this.doPay(order.id)
              } else {
                uni.redirectTo({ url: '/subB/pages/orders/detail?id=' + order.id })
              }
            },
          })
        })
        .catch(() => {})
        .finally(() => {
          this.submitting = false
        })
    },
    doPay(orderId) {
      api
        .payOrder(orderId)
        .then((res) => {
          uni.showToast({ title: '支付成功', icon: 'success' })
          setTimeout(() => {
            uni.redirectTo({ url: '/subB/pages/orders/detail?id=' + orderId })
          }, 800)
        })
        .catch(() => {})
    },
  },
}
</script>

<style scoped lang="scss">
.page {
  padding-bottom: 160rpx;
}

.order-title {
  font-size: 34rpx;
  font-weight: 700;
  margin-bottom: 20rpx;
}

.order-row {
  display: flex;
  margin-top: 16rpx;
  font-size: 28rpx;

  .label {
    color: #999;
    width: 100rpx;
    flex-shrink: 0;
  }

  .value {
    color: #333;
    flex: 1;

    &.price {
      color: #ff4d4f;
      font-weight: 700;
    }
  }
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  margin-bottom: 20rpx;
}

.remark-input {
  width: 100%;
  height: 160rpx;
  background: #f7f8fa;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 24rpx;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.06);

  .bottom-price {
    display: flex;
    align-items: baseline;

    .label {
      font-size: 26rpx;
      color: #666;
      margin-right: 12rpx;
    }

    .price {
      font-size: 40rpx;
    }
  }

  .submit-btn {
    background: linear-gradient(135deg, #ff6b35, #ff4d4f);
    color: #fff;
    border-radius: 48rpx;
    padding: 20rpx 64rpx;
    font-size: 30rpx;
    font-weight: 600;

    &.disabled {
      background: #ccc;
    }
  }
}
</style>
