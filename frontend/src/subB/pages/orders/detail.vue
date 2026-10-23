<template>
  <view class="page" v-if="order">
    <!-- 状态横幅 -->
    <view class="status-banner" :class="order.status">
      <view class="status-icon">{{ statusIcon }}</view>
      <view class="status-text">{{ order.status_display }}</view>
      <view class="status-desc">{{ statusDesc }}</view>
    </view>

    <!-- 验票码（已支付/已使用） -->
    <view class="card ticket-card" v-if="order.status === 'paid' || order.status === 'used'">
      <view class="section-title">电子票验票码</view>
      <view class="ticket-code">{{ order.ticket_code || '—' }}</view>
      <view class="ticket-tip">入场时请向工作人员出示此验票码核销</view>
      <view class="copy-btn" @click="copyCode">复制验票码</view>
    </view>

    <!-- 订单信息 -->
    <view class="card">
      <view class="section-title">订单信息</view>
      <view class="info-row">
        <text class="label">活动</text>
        <text class="value">{{ order.event_title }}</text>
      </view>
      <view class="info-row">
        <text class="label">场次</text>
        <text class="value">{{ order.session_name }}（{{ formatTime(order.session_start_time) }}）</text>
      </view>
      <view class="info-row">
        <text class="label">票档</text>
        <text class="value">{{ order.ticket_type_name }} ¥{{ order.unit_price }}</text>
      </view>
      <view class="info-row">
        <text class="label">数量</text>
        <text class="value">{{ order.quantity }} 张</text>
      </view>
      <view class="info-row">
        <text class="label">订单金额</text>
        <text class="value price">¥{{ order.amount }}</text>
      </view>
      <view class="info-row">
        <text class="label">下单时间</text>
        <text class="value">{{ formatTime(order.created_at) }}</text>
      </view>
      <view class="info-row" v-if="order.paid_at">
        <text class="label">支付时间</text>
        <text class="value">{{ formatTime(order.paid_at) }}</text>
      </view>
      <view class="info-row" v-if="order.used_at">
        <text class="label">核销时间</text>
        <text class="value">{{ formatTime(order.used_at) }}</text>
      </view>
      <view class="info-row" v-if="order.remark">
        <text class="label">备注</text>
        <text class="value">{{ order.remark }}</text>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-bar safe-bottom" v-if="order.status === 'pending'">
      <view class="action-btn cancel" @click="cancelOrder">取消订单</view>
      <view class="action-btn pay" @click="payOrder">立即支付 ¥{{ order.amount }}</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../../api/index.js'

export default {
  data() {
    return {
      orderId: null,
      order: null,
    }
  },
  computed: {
    statusIcon() {
      const map = {
        pending: '⏳',
        paid: '🎫',
        used: '✅',
        cancelled: '✖️',
        refunded: '↩️',
      }
      return map[this.order ? this.order.status : ''] || '📋'
    },
    statusDesc() {
      const map = {
        pending: '订单待支付，请尽快完成支付',
        paid: '支付成功，凭验票码入场',
        used: '该订单已完成验票核销',
        cancelled: '订单已取消，如需购票请重新下单',
        refunded: '订单已退款',
      }
      return map[this.order ? this.order.status : ''] || ''
    },
  },
  onLoad(options) {
    this.orderId = options.id
  },
  onShow() {
    if (this.orderId) {
      this.loadDetail()
    }
  },
  methods: {
    formatTime(t) {
      if (!t) return ''
      return String(t).replace('T', ' ').slice(0, 19)
    },
    loadDetail() {
      api
        .getOrderDetail(this.orderId)
        .then((res) => {
          this.order = res.data
        })
        .catch(() => {})
    },
    copyCode() {
      if (!this.order.ticket_code) return
      uni.setClipboardData({
        data: this.order.ticket_code,
        success: () => uni.showToast({ title: '已复制', icon: 'success' }),
      })
    },
    payOrder() {
      uni.showModal({
        title: '模拟支付',
        content: `确认支付 ¥${this.order.amount}？`,
        success: (r) => {
          if (r.confirm) {
            api
              .payOrder(this.order.id)
              .then(() => {
                uni.showToast({ title: '支付成功', icon: 'success' })
                this.loadDetail()
              })
              .catch(() => {})
          }
        },
      })
    },
    cancelOrder() {
      uni.showModal({
        title: '取消订单',
        content: '确定取消该订单吗？取消后库存将释放。',
        success: (r) => {
          if (r.confirm) {
            api
              .cancelOrder(this.order.id)
              .then(() => {
                uni.showToast({ title: '已取消', icon: 'success' })
                this.loadDetail()
              })
              .catch(() => {})
          }
        },
      })
    },
  },
}
</script>

<style scoped lang="scss">
.page {
  padding-bottom: 160rpx;
}

.status-banner {
  padding: 60rpx 24rpx;
  text-align: center;

  .status-icon {
    font-size: 80rpx;
  }

  .status-text {
    font-size: 38rpx;
    font-weight: 700;
    margin-top: 16rpx;
    color: #333;
  }

  .status-desc {
    font-size: 24rpx;
    color: #999;
    margin-top: 12rpx;
  }
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  margin-bottom: 20rpx;
}

.ticket-card {
  text-align: center;

  .ticket-code {
    font-size: 48rpx;
    font-weight: 800;
    letter-spacing: 8rpx;
    color: #333;
    padding: 20rpx 0;
    background: #fafafa;
    border-radius: 12rpx;
    border: 2rpx dashed #ddd;
  }

  .ticket-tip {
    font-size: 24rpx;
    color: #999;
    margin-top: 16rpx;
  }

  .copy-btn {
    display: inline-block;
    margin-top: 20rpx;
    font-size: 26rpx;
    color: #1677ff;
    border: 1rpx solid #1677ff;
    border-radius: 30rpx;
    padding: 10rpx 40rpx;
  }
}

.info-row {
  display: flex;
  margin-top: 16rpx;
  font-size: 28rpx;

  .label {
    color: #999;
    width: 140rpx;
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

.action-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  display: flex;
  padding: 20rpx 24rpx;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.06);

  .action-btn {
    flex: 1;
    text-align: center;
    border-radius: 48rpx;
    padding: 20rpx 0;
    font-size: 30rpx;
    font-weight: 600;

    &.cancel {
      border: 1rpx solid #ddd;
      color: #666;
      margin-right: 20rpx;
    }

    &.pay {
      background: linear-gradient(135deg, #ff6b35, #ff4d4f);
      color: #fff;
    }
  }
}
</style>
