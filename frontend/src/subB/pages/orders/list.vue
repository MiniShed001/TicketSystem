<template>
  <view class="page">
    <!-- 状态筛选 -->
    <view class="status-tabs">
      <view
        v-for="s in statusTabs"
        :key="s.key"
        class="status-tab"
        :class="{ active: currentStatus === s.key }"
        @click="switchStatus(s.key)"
      >
        {{ s.label }}
      </view>
    </view>

    <!-- 订单列表 -->
    <view v-if="orders.length" class="order-list">
      <view v-for="o in orders" :key="o.id" class="order-card" @click="goDetail(o.id)">
        <view class="order-head">
          <text class="order-no">订单号 {{ o.order_no }}</text>
          <text class="order-status" :class="o.status">{{ o.status_display }}</text>
        </view>
        <view class="order-body">
          <image class="order-cover" :src="o.cover_url || '/static/logo.png'" mode="aspectFill" />
          <view class="order-info">
            <view class="order-event">{{ o.event_title }}</view>
            <view class="order-meta">{{ o.session_name }} · {{ o.ticket_type_name }} × {{ o.quantity }}</view>
            <view class="order-time">{{ formatTime(o.session_start_time) }}</view>
          </view>
        </view>
        <view class="order-foot">
          <text class="order-amount">¥{{ o.amount }}</text>
          <view class="order-actions">
            <view v-if="o.status === 'pending'" class="mini-btn pay" @click.stop="payOrder(o)">去支付</view>
            <view v-if="o.status === 'pending'" class="mini-btn cancel" @click.stop="cancelOrder(o)">取消</view>
            <view v-if="o.status === 'paid'" class="mini-btn ticket" @click.stop="goDetail(o.id)">查看验票码</view>
          </view>
        </view>
      </view>
      <view class="load-more">{{ hasMore ? '上拉加载更多' : '没有更多了' }}</view>
    </view>

    <view v-else-if="!loading" class="empty-box">暂无订单，快去购票吧</view>
    <view v-else class="empty-box">加载中...</view>
  </view>
</template>

<script>
import { api } from '../../../api/index.js'

const STATUS_TABS = [
  { key: '', label: '全部' },
  { key: 'pending', label: '待支付' },
  { key: 'paid', label: '已支付' },
  { key: 'used', label: '已使用' },
  { key: 'cancelled', label: '已取消' },
]

export default {
  data() {
    return {
      statusTabs: STATUS_TABS,
      currentStatus: '',
      orders: [],
      page: 1,
      pageSize: 10,
      hasMore: true,
      loading: false,
    }
  },
  onShow() {
    this.loadOrders(true)
  },
  onPullDownRefresh() {
    this.loadOrders(true).finally(() => uni.stopPullDownRefresh())
  },
  onReachBottom() {
    if (this.hasMore && !this.loading) {
      this.loadOrders(false)
    }
  },
  methods: {
    formatTime(t) {
      if (!t) return ''
      return String(t).replace('T', ' ').slice(0, 16)
    },
    switchStatus(key) {
      if (this.currentStatus === key) return
      this.currentStatus = key
      this.loadOrders(true)
    },
    goDetail(id) {
      uni.navigateTo({ url: `/subB/pages/orders/detail?id=${id}` })
    },
    loadOrders(reset) {
      if (this.loading) return Promise.resolve()
      this.loading = true
      const params = { page: reset ? 1 : this.page, page_size: this.pageSize }
      if (this.currentStatus) params.status = this.currentStatus
      return api
        .getOrders(params)
        .then((res) => {
          const data = res.data
          const list = data.results || []
          this.orders = reset ? list : this.orders.concat(list)
          this.page = reset ? 2 : this.page + 1
          this.hasMore = this.orders.length < data.count
        })
        .catch(() => {})
        .finally(() => {
          this.loading = false
        })
    },
    payOrder(order) {
      uni.showModal({
        title: '模拟支付',
        content: `确认支付 ¥${order.amount}？`,
        success: (r) => {
          if (r.confirm) {
            api
              .payOrder(order.id)
              .then(() => {
                uni.showToast({ title: '支付成功', icon: 'success' })
                this.loadOrders(true)
              })
              .catch(() => {})
          }
        },
      })
    },
    cancelOrder(order) {
      uni.showModal({
        title: '取消订单',
        content: '确定取消该订单吗？取消后库存将释放。',
        success: (r) => {
          if (r.confirm) {
            api
              .cancelOrder(order.id)
              .then(() => {
                uni.showToast({ title: '已取消', icon: 'success' })
                this.loadOrders(true)
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
  padding-bottom: 40rpx;
}

.status-tabs {
  display: flex;
  background: #fff;
  padding: 16rpx 0;
  position: sticky;
  top: 0;
  z-index: 10;

  .status-tab {
    flex: 1;
    text-align: center;
    font-size: 26rpx;
    color: #666;
    padding: 10rpx 0;
    position: relative;

    &.active {
      color: #ff4d4f;
      font-weight: 600;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40rpx;
        height: 6rpx;
        border-radius: 3rpx;
        background: #ff4d4f;
      }
    }
  }
}

.order-card {
  background: #fff;
  margin: 20rpx 24rpx;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.order-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16rpx;
  border-bottom: 1rpx solid #f0f0f0;

  .order-no {
    font-size: 24rpx;
    color: #999;
  }

  .order-status {
    font-size: 26rpx;
    font-weight: 600;

    &.pending {
      color: #ff8c00;
    }

    &.paid {
      color: #00b578;
    }

    &.used {
      color: #1677ff;
    }

    &.cancelled {
      color: #999;
    }
  }
}

.order-body {
  display: flex;
  padding: 20rpx 0;

  .order-cover {
    width: 140rpx;
    height: 140rpx;
    border-radius: 10rpx;
    flex-shrink: 0;
  }

  .order-info {
    flex: 1;
    margin-left: 20rpx;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
  }

  .order-event {
    font-size: 28rpx;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .order-meta {
    font-size: 24rpx;
    color: #888;
    margin-top: 10rpx;
  }

  .order-time {
    font-size: 24rpx;
    color: #999;
    margin-top: 8rpx;
  }
}

.order-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16rpx;
  border-top: 1rpx solid #f0f0f0;

  .order-amount {
    font-size: 32rpx;
    color: #ff4d4f;
    font-weight: 700;
  }

  .order-actions {
    display: flex;

    .mini-btn {
      font-size: 24rpx;
      border-radius: 30rpx;
      padding: 10rpx 28rpx;
      margin-left: 16rpx;

      &.pay {
        background: linear-gradient(135deg, #ff6b35, #ff4d4f);
        color: #fff;
      }

      &.cancel {
        border: 1rpx solid #ddd;
        color: #666;
      }

      &.ticket {
        border: 1rpx solid #1677ff;
        color: #1677ff;
      }
    }
  }
}

.load-more {
  text-align: center;
  color: #aaa;
  font-size: 24rpx;
  padding: 24rpx 0;
}
</style>
