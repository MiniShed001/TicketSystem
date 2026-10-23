<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input">
        <text class="search-icon">🔍</text>
        <input
          v-model="keyword"
          placeholder="搜索活动 / 场馆 / 城市"
          confirm-type="search"
          @confirm="onSearch"
        />
      </view>
    </view>

    <!-- 分类 -->
    <scroll-view class="cat-scroll" scroll-x :show-scrollbar="false">
      <view class="cat-list">
        <view
          v-for="c in categories"
          :key="c.key"
          class="cat-item"
          :class="{ active: currentCat === c.key }"
          @click="onCategory(c.key)"
        >
          {{ c.label }}
        </view>
      </view>
    </scroll-view>

    <!-- 活动列表 -->
    <view v-if="events.length" class="event-list">
      <view
        v-for="e in events"
        :key="e.id"
        class="event-card"
        @click="goDetail(e.id)"
      >
        <image class="event-cover" :src="e.cover_url || '/static/logo.png'" mode="aspectFill" />
        <view class="event-info">
          <view class="event-title">{{ e.title }}</view>
          <view class="event-meta">
            <text class="tag">{{ categoryLabel(e.category) }}</text>
            <text class="meta-text">{{ e.city }} · {{ e.venue }}</text>
          </view>
          <view class="event-time">{{ formatTime(e.start_time) }}</view>
          <view class="event-bottom">
            <text class="price" v-if="e.min_price != null">¥{{ e.min_price }} 起</text>
            <text class="hot-tag" v-if="e.is_hot">🔥 热门</text>
          </view>
        </view>
      </view>
      <view class="load-more">{{ hasMore ? '上拉加载更多' : '没有更多了' }}</view>
    </view>

    <view v-else-if="!loading" class="empty-box">暂无相关活动</view>
    <view v-else class="empty-box">加载中...</view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

const CATEGORIES = [
  { key: '', label: '全部' },
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
      categories: CATEGORIES,
      currentCat: '',
      keyword: '',
      events: [],
      page: 1,
      pageSize: 10,
      hasMore: true,
      loading: false,
    }
  },
  onLoad() {
    this.loadEvents(true)
  },
  onPullDownRefresh() {
    this.loadEvents(true).finally(() => uni.stopPullDownRefresh())
  },
  onReachBottom() {
    if (this.hasMore && !this.loading) {
      this.loadEvents(false)
    }
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
    onSearch() {
      this.loadEvents(true)
    },
    onCategory(key) {
      if (this.currentCat === key) return
      this.currentCat = key
      this.loadEvents(true)
    },
    goDetail(id) {
      uni.navigateTo({ url: `/subA/pages/detail/detail?id=${id}` })
    },
    loadEvents(reset) {
      if (this.loading) return Promise.resolve()
      this.loading = true
      const params = {
        page: reset ? 1 : this.page,
        page_size: this.pageSize,
      }
      if (this.currentCat) params.category = this.currentCat
      if (this.keyword) params.q = this.keyword
      return api
        .getEvents(params)
        .then((res) => {
          const data = res.data
          const list = data.results || []
          this.events = reset ? list : this.events.concat(list)
          this.page = reset ? 2 : this.page + 1
          this.hasMore = this.events.length < data.count
        })
        .catch(() => {})
        .finally(() => {
          this.loading = false
        })
    },
  },
}
</script>

<style scoped lang="scss">
.page {
  padding-bottom: 40rpx;
}

.search-bar {
  padding: 20rpx 24rpx 10rpx;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.search-input {
  display: flex;
  align-items: center;
  background: #f2f3f5;
  border-radius: 40rpx;
  padding: 16rpx 24rpx;
  font-size: 28rpx;

  .search-icon {
    margin-right: 12rpx;
    font-size: 26rpx;
  }

  input {
    flex: 1;
  }
}

.cat-scroll {
  background: #fff;
  white-space: nowrap;
  padding-bottom: 16rpx;
}

.cat-list {
  display: inline-flex;
  padding: 0 16rpx;
}

.cat-item {
  padding: 10rpx 28rpx;
  margin: 0 8rpx;
  border-radius: 32rpx;
  font-size: 26rpx;
  color: #555;
  background: #f5f6fa;

  &.active {
    background: linear-gradient(135deg, #ff6b35, #ff4d4f);
    color: #fff;
    font-weight: 600;
  }
}

.event-list {
  padding: 10rpx 0;
}

.event-card {
  display: flex;
  background: #fff;
  margin: 20rpx 24rpx;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);

  .event-cover {
    width: 240rpx;
    height: 240rpx;
    flex-shrink: 0;
  }

  .event-info {
    flex: 1;
    padding: 20rpx 24rpx;
    display: flex;
    flex-direction: column;
  }

  .event-title {
    font-size: 30rpx;
    font-weight: 600;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .event-meta {
    margin-top: 12rpx;
    display: flex;
    align-items: center;

    .tag {
      font-size: 22rpx;
      color: #ff4d4f;
      background: #fff1f0;
      border-radius: 6rpx;
      padding: 2rpx 10rpx;
      margin-right: 12rpx;
      flex-shrink: 0;
    }

    .meta-text {
      font-size: 24rpx;
      color: #888;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }

  .event-time {
    margin-top: 10rpx;
    font-size: 24rpx;
    color: #666;
  }

  .event-bottom {
    margin-top: auto;
    padding-top: 12rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .price {
      font-size: 32rpx;
    }

    .hot-tag {
      font-size: 22rpx;
      color: #ff8c00;
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
