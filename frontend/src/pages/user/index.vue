<template>
  <view class="page">
    <!-- 用户信息 -->
    <view class="user-header">
      <view class="avatar-box">
        <image
          v-if="$user.userInfo && $user.userInfo.avatar_url"
          class="avatar"
          :src="$user.userInfo.avatar_url"
          mode="aspectFill"
        />
        <view v-else class="avatar avatar-default">{{ avatarText }}</view>
      </view>
      <view class="user-info" v-if="$user.isLogin">
        <view class="user-name">{{ nickname }}</view>
        <view class="user-account">@{{ username }}</view>
      </view>
      <view class="user-info" v-else @click="goLogin">
        <view class="user-name">点击登录</view>
        <view class="user-account">登录后享受购票服务</view>
      </view>
    </view>

    <!-- 订单入口 -->
    <view class="card menu-card">
      <view class="menu-title">我的订单</view>
      <view class="order-menu">
        <view class="menu-item" @click="goOrders('')">
          <view class="menu-icon">📋</view>
          <view class="menu-label">全部</view>
        </view>
        <view class="menu-item" @click="goOrders('pending')">
          <view class="menu-icon">⏳</view>
          <view class="menu-label">待支付</view>
        </view>
        <view class="menu-item" @click="goOrders('paid')">
          <view class="menu-icon">🎫</view>
          <view class="menu-label">已支付</view>
        </view>
        <view class="menu-item" @click="goOrders('used')">
          <view class="menu-icon">✅</view>
          <view class="menu-label">已使用</view>
        </view>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="card menu-card" v-if="$user.isLogin">
      <view class="menu-row" @click="editProfile">
        <text>编辑资料</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-row" @click="logout">
        <text class="danger">退出登录</text>
        <text class="arrow">›</text>
      </view>
    </view>

    <view class="version">票务系统 v1.0.0</view>
  </view>
</template>

<script>
export default {
  computed: {
    nickname() {
      const u = this.$user.userInfo
      return (u && (u.nickname || u.username)) || '用户'
    },
    username() {
      const u = this.$user.userInfo
      return (u && u.username) || ''
    },
    avatarText() {
      return this.nickname.slice(0, 1)
    },
  },
  onShow() {
    // 刷新用户信息
    if (this.$user.isLogin) {
      this.refreshUser()
    }
  },
  methods: {
    refreshUser() {
      // 从缓存直接取，避免频繁请求；如需最新信息可放开下面接口
      // import { api } from '../../api/index.js'
      // api.getUserInfo().then((res) => this.$user.setUserInfo(res.data))
    },
    goLogin() {
      uni.navigateTo({ url: '/pages/login/login' })
    },
    goOrders(status) {
      if (!this.$user.isLogin) {
        uni.navigateTo({ url: '/pages/login/login' })
        return
      }
      const url = status
        ? `/subB/pages/orders/list?status=${status}`
        : '/subB/pages/orders/list'
      uni.navigateTo({ url })
    },
    editProfile() {
      uni.showToast({ title: '个人资料编辑功能开发中', icon: 'none' })
    },
    logout() {
      uni.showModal({
        title: '退出登录',
        content: '确定退出当前账号吗？',
        success: (r) => {
          if (r.confirm) {
            this.$user.logout()
            uni.showToast({ title: '已退出', icon: 'success' })
          }
        },
      })
    },
  },
}
</script>

<style scoped lang="scss">
.page {
  padding-bottom: 60rpx;
}

.user-header {
  display: flex;
  align-items: center;
  padding: 60rpx 40rpx;
  background: linear-gradient(135deg, #ff6b35, #ff4d4f);

  .avatar-box {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    overflow: hidden;
    border: 4rpx solid rgba(255, 255, 255, 0.6);
    flex-shrink: 0;

    .avatar {
      width: 100%;
      height: 100%;
    }

    .avatar-default {
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(255, 255, 255, 0.25);
      color: #fff;
      font-size: 48rpx;
      font-weight: 700;
    }
  }

  .user-info {
    margin-left: 28rpx;
    color: #fff;
    flex: 1;

    .user-name {
      font-size: 36rpx;
      font-weight: 700;
    }

    .user-account {
      font-size: 24rpx;
      opacity: 0.85;
      margin-top: 8rpx;
    }
  }
}

.menu-card {
  .menu-title {
    font-size: 30rpx;
    font-weight: 600;
    margin-bottom: 24rpx;
  }
}

.order-menu {
  display: flex;

  .menu-item {
    flex: 1;
    text-align: center;

    .menu-icon {
      font-size: 48rpx;
    }

    .menu-label {
      font-size: 24rpx;
      color: #666;
      margin-top: 10rpx;
    }
  }
}

.menu-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 8rpx;
  border-bottom: 1rpx solid #f5f5f5;
  font-size: 28rpx;

  &:last-child {
    border-bottom: none;
  }

  .danger {
    color: #ff4d4f;
  }

  .arrow {
    color: #ccc;
    font-size: 32rpx;
  }
}

.version {
  text-align: center;
  color: #ccc;
  font-size: 22rpx;
  margin-top: 60rpx;
}
</style>
