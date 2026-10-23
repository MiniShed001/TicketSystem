<template>
  <view class="page" v-if="event">
    <!-- 封面 -->
    <image class="hero" :src="event.cover_url || '/static/logo.png'" mode="aspectFill" />

    <!-- 基本信息 -->
    <view class="card info-card">
      <view class="event-title">{{ event.title }}</view>
      <view class="tag-row">
        <text class="tag">{{ categoryLabel(event.category) }}</text>
        <text class="tag hot" v-if="event.is_hot">热门</text>
      </view>
      <view class="info-row">
        <text class="label">场馆</text>
        <text class="value">{{ event.venue }}</text>
      </view>
      <view class="info-row">
        <text class="label">地址</text>
        <text class="value">{{ event.city }} {{ event.address }}</text>
      </view>
      <view class="info-row">
        <text class="label">时间</text>
        <text class="value">{{ formatTime(event.start_time) }} ~ {{ formatTime(event.end_time) }}</text>
      </view>
    </view>

    <!-- 场次选择 -->
    <view class="card">
      <view class="section-title">选择场次</view>
      <view class="session-list">
        <view
          v-for="s in event.sessions"
          :key="s.id"
          class="session-item"
          :class="{ active: selectedSession && selectedSession.id === s.id, disabled: s.status !== 'open' }"
          @click="selectSession(s)"
        >
          <view class="session-name">{{ s.name }}</view>
          <view class="session-time">{{ formatTime(s.start_time) }}</view>
          <view class="session-status">{{ sessionStatusText(s) }}</view>
        </view>
      </view>
    </view>

    <!-- 票档选择 -->
    <view class="card" v-if="selectedSession">
      <view class="section-title">选择票档</view>
      <view
        v-for="t in selectedSession.ticket_types"
        :key="t.id"
        class="ticket-item"
        :class="{ active: selectedTicket && selectedTicket.id === t.id, disabled: t.remain_count <= 0 }"
        @click="selectTicket(t)"
      >
        <view class="ticket-left">
          <view class="ticket-name">{{ t.name }}</view>
          <view class="ticket-desc">{{ t.description || '普通区域' }}</view>
        </view>
        <view class="ticket-right">
          <view class="ticket-price">¥{{ t.price }}</view>
          <view class="ticket-remain">余 {{ t.remain_count }} 张</view>
        </view>
      </view>
    </view>

    <!-- 数量选择 -->
    <view class="card" v-if="selectedTicket">
      <view class="section-title">购票数量</view>
      <view class="qty-row">
        <view class="qty-btn" :class="{ disabled: qty <= 1 }" @click="changeQty(-1)">−</view>
        <view class="qty-num">{{ qty }}</view>
        <view class="qty-btn" :class="{ disabled: qty >= maxQty }" @click="changeQty(1)">＋</view>
        <view class="qty-tip">每人限购 10 张，当前余 {{ selectedTicket.remain_count }} 张</view>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar safe-bottom">
      <view class="bottom-price">
        <text class="price" v-if="selectedTicket">¥{{ totalAmount }}</text>
        <text class="price-tip" v-else>请选择票档</text>
      </view>
      <view class="buy-btn" :class="{ disabled: !canBuy }" @click="goConfirm">立即购买</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../../api/index.js'

const CATEGORIES = [
  { key: 'concert', label: '演唱会' },
  { key: 'drama', label: '话剧' },
  { key: 'exhibition', label: '展览' },
  { key: 'movie', label: '电影' },
  { key: 'sports', label: '体育' },
  { key: 'other', label: '其他' },
]

export default {
  data() {
    return {
      eventId: null,
      event: null,
      selectedSession: null,
      selectedTicket: null,
      qty: 1,
      maxQty: 10,
    }
  },
  computed: {
    totalAmount() {
      if (!this.selectedTicket) return '0'
      return (parseFloat(this.selectedTicket.price) * this.qty).toFixed(2)
    },
    canBuy() {
      return !!(this.event && this.selectedSession && this.selectedTicket && this.selectedTicket.remain_count > 0)
    },
  },
  onLoad(options) {
    this.eventId = options.id
    this.loadDetail()
  },
  methods: {
    categoryLabel(key) {
      const c = CATEGORIES.find((i) => i.key === key)
      return c ? c.label : '其他'
    },
    formatTime(t) {
      if (!t) return ''
      return String(t).replace('T', ' ').slice(0, 16)
    },
    sessionStatusText(s) {
      if (s.status === 'open') return '售票中'
      if (s.status === 'soldout') return '已售罄'
      return '已结束'
    },
    loadDetail() {
      api
        .getEventDetail(this.eventId)
        .then((res) => {
          this.event = res.data
          // 默认选中第一个售票中场次
          const firstOpen = this.event.sessions.find((s) => s.status === 'open')
          if (firstOpen) {
            this.selectSession(firstOpen)
          }
        })
        .catch(() => {})
    },
    selectSession(s) {
      if (s.status !== 'open') return
      this.selectedSession = s
      this.selectedTicket = null
      this.qty = 1
    },
    selectTicket(t) {
      if (t.remain_count <= 0) return
      this.selectedTicket = t
      this.maxQty = Math.min(10, t.remain_count)
      if (this.qty > this.maxQty) this.qty = this.maxQty
    },
    changeQty(delta) {
      const next = this.qty + delta
      if (next < 1 || next > this.maxQty) return
      this.qty = next
    },
    goConfirm() {
      if (!this.canBuy) {
        uni.showToast({ title: '请先选择场次和票档', icon: 'none' })
        return
      }
      const ev = this.event
      const s = this.selectedSession
      const t = this.selectedTicket
      const params = [
        `session_id=${s.id}`,
        `ticket_type_id=${t.id}`,
        `qty=${this.qty}`,
        `amount=${this.totalAmount}`,
        `event_title=${encodeURIComponent(ev.title)}`,
        `session_name=${encodeURIComponent(s.name)}`,
        `start_time=${encodeURIComponent(s.start_time)}`,
        `ticket_name=${encodeURIComponent(t.name)}`,
        `ticket_price=${t.price}`,
        `venue=${encodeURIComponent(ev.venue)}`,
        `city=${encodeURIComponent(ev.city)}`,
      ]
      uni.navigateTo({ url: `/subA/pages/order/confirm?${params.join('&')}` })
    },
  },
}
</script>

<style scoped lang="scss">
.page {
  padding-bottom: 160rpx;
}

.hero {
  width: 30%;
  height: auto;
  aspect-ratio: 16 / 9;
  background-color: #eef2f7;
}

.info-card {
  .event-title {
    font-size: 36rpx;
    font-weight: 700;
    line-height: 1.4;
  }

  .tag-row {
    margin: 16rpx 0;
  }

  .tag {
    font-size: 22rpx;
    color: #ff4d4f;
    background: #fff1f0;
    border-radius: 6rpx;
    padding: 4rpx 12rpx;
    margin-right: 12rpx;

    &.hot {
      color: #ff8c00;
      background: #fff7e6;
    }
  }

  .info-row {
    display: flex;
    margin-top: 12rpx;
    font-size: 26rpx;

    .label {
      color: #999;
      width: 90rpx;
      flex-shrink: 0;
    }

    .value {
      color: #333;
      flex: 1;
    }
  }
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  margin-bottom: 20rpx;
}

.session-item {
  border: 2rpx solid #e5e6eb;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  margin-bottom: 16rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;

  &.active {
    border-color: #ff4d4f;
    background: #fff8f7;
  }

  &.disabled {
    opacity: 0.5;
  }

  .session-name {
    font-size: 28rpx;
    font-weight: 600;
  }

  .session-time {
    font-size: 24rpx;
    color: #888;
    margin-top: 6rpx;
  }

  .session-status {
    font-size: 24rpx;
    color: #ff4d4f;
  }
}

.ticket-item {
  border: 2rpx solid #e5e6eb;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;

  &.active {
    border-color: #ff4d4f;
    background: #fff8f7;
  }

  &.disabled {
    opacity: 0.5;
  }

  .ticket-name {
    font-size: 30rpx;
    font-weight: 600;
  }

  .ticket-desc {
    font-size: 24rpx;
    color: #999;
    margin-top: 8rpx;
  }

  .ticket-price {
    font-size: 36rpx;
    color: #ff4d4f;
    font-weight: 700;
    text-align: right;
  }

  .ticket-remain {
    font-size: 22rpx;
    color: #999;
    margin-top: 6rpx;
    text-align: right;
  }
}

.qty-row {
  display: flex;
  align-items: center;

  .qty-btn {
    width: 64rpx;
    height: 64rpx;
    line-height: 60rpx;
    text-align: center;
    border: 2rpx solid #e5e6eb;
    border-radius: 50%;
    font-size: 36rpx;
    color: #333;
    background: #fff;

    &.disabled {
      color: #ccc;
    }
  }

  .qty-num {
    width: 100rpx;
    text-align: center;
    font-size: 34rpx;
    font-weight: 600;
  }

  .qty-tip {
    margin-left: 24rpx;
    font-size: 24rpx;
    color: #999;
  }
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
    .price {
      font-size: 40rpx;
    }

    .price-tip {
      font-size: 28rpx;
      color: #999;
    }
  }

  .buy-btn {
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
