<template>
  <view class="page">
    <view class="brand">
      <view class="brand-logo">🎫</view>
      <view class="brand-name">票务系统</view>
      <view class="brand-slogan">好演出，不错过</view>
    </view>

    <view class="form-card">
      <!-- 模式切换 -->
      <view class="mode-tabs">
        <view class="mode-tab" :class="{ active: mode === 'login' }" @click="mode = 'login'">登录</view>
        <view class="mode-tab" :class="{ active: mode === 'register' }" @click="mode = 'register'">注册</view>
      </view>

      <!-- 表单 -->
      <view class="form-item">
        <text class="form-label">用户名</text>
        <input v-model="form.username" class="form-input" placeholder="请输入用户名" :maxlength="32" />
      </view>

      <view class="form-item" v-if="mode === 'register'">
        <text class="form-label">昵称</text>
        <input v-model="form.nickname" class="form-input" placeholder="选填" :maxlength="32" />
      </view>

      <view class="form-item">
        <text class="form-label">密码</text>
        <input
          v-model="form.password"
          class="form-input"
          placeholder="请输入密码（至少 6 位）"
          :password="!showPwd"
          :maxlength="64"
        />
      </view>

      <view class="form-item" v-if="mode === 'register'">
        <text class="form-label">确认密码</text>
        <input
          v-model="form.confirm_password"
          class="form-input"
          placeholder="请再次输入密码"
          :password="!showPwd"
          :maxlength="64"
        />
      </view>

      <view class="form-item" v-if="mode === 'register'">
        <text class="form-label">手机号</text>
        <input v-model="form.phone" class="form-input" placeholder="选填" type="number" :maxlength="11" />
      </view>

      <view class="submit-btn" :class="{ disabled: submitting }" @click="submit">
        {{ submitting ? '提交中...' : mode === 'login' ? '登 录' : '注 册' }}
      </view>

      <view class="demo-tip">演示账号：demo / demo123456</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      mode: 'login',
      form: {
        username: '',
        nickname: '',
        password: '',
        confirm_password: '',
        phone: '',
      },
      showPwd: false,
      submitting: false,
    }
  },
  onLoad(options) {
    if (options.mode === 'register') {
      this.mode = 'register'
    }
  },
  methods: {
    submit() {
      if (this.submitting) return
      const f = this.form
      if (!f.username.trim()) {
        uni.showToast({ title: '请输入用户名', icon: 'none' })
        return
      }
      if (!f.password) {
        uni.showToast({ title: '请输入密码', icon: 'none' })
        return
      }
      if (this.mode === 'login') {
        this.doLogin()
      } else {
        if (f.password !== f.confirm_password) {
          uni.showToast({ title: '两次密码不一致', icon: 'none' })
          return
        }
        this.doRegister()
      }
    },
    doLogin() {
      this.submitting = true
      api
        .login({ username: this.form.username, password: this.form.password })
        .then((res) => {
          this.$user.setLogin(res.data.tokens, res.data.user)
          uni.showToast({ title: '登录成功', icon: 'success' })
          setTimeout(() => this.back(), 600)
        })
        .catch(() => {})
        .finally(() => {
          this.submitting = false
        })
    },
    doRegister() {
      this.submitting = true
      api
        .register({
          username: this.form.username,
          nickname: this.form.nickname,
          password: this.form.password,
          confirm_password: this.form.confirm_password,
          phone: this.form.phone || undefined,
        })
        .then((res) => {
          this.$user.setLogin(res.data.tokens, res.data.user)
          uni.showToast({ title: '注册成功', icon: 'success' })
          setTimeout(() => this.back(), 600)
        })
        .catch(() => {})
        .finally(() => {
          this.submitting = false
        })
    },
    back() {
      const pages = getCurrentPages()
      if (pages.length > 1) {
        uni.navigateBack()
      } else {
        uni.switchTab({ url: '/pages/index/index' })
      }
    },
  },
}
</script>

<style scoped lang="scss">
.page {
  min-height: 100vh;
  background: linear-gradient(180deg, #fff5f3 0%, #f5f6fa 60%);
  padding: 0 48rpx;
}

.brand {
  text-align: center;
  padding: 100rpx 0 60rpx;

  .brand-logo {
    font-size: 100rpx;
  }

  .brand-name {
    font-size: 44rpx;
    font-weight: 800;
    margin-top: 16rpx;
    background: linear-gradient(135deg, #ff6b35, #ff4d4f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .brand-slogan {
    font-size: 26rpx;
    color: #999;
    margin-top: 12rpx;
  }
}

.form-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx 36rpx;
  box-shadow: 0 8rpx 32rpx rgba(255, 77, 79, 0.08);
}

.mode-tabs {
  display: flex;
  margin-bottom: 40rpx;
  border-bottom: 1rpx solid #f0f0f0;

  .mode-tab {
    flex: 1;
    text-align: center;
    font-size: 32rpx;
    color: #999;
    padding: 16rpx 0;
    position: relative;

    &.active {
      color: #ff4d4f;
      font-weight: 700;

      &::after {
        content: '';
        position: absolute;
        bottom: -1rpx;
        left: 50%;
        transform: translateX(-50%);
        width: 60rpx;
        height: 6rpx;
        border-radius: 3rpx;
        background: #ff4d4f;
      }
    }
  }
}

.form-item {
  margin-bottom: 28rpx;

  .form-label {
    display: block;
    font-size: 26rpx;
    color: #666;
    margin-bottom: 12rpx;
  }

  .form-input {
    background: #f7f8fa;
    border-radius: 12rpx;
    padding: 20rpx 24rpx;
    font-size: 30rpx;
  }
}

.submit-btn {
  margin-top: 40rpx;
  background: linear-gradient(135deg, #ff6b35, #ff4d4f);
  color: #fff;
  border-radius: 48rpx;
  padding: 24rpx 0;
  text-align: center;
  font-size: 32rpx;
  font-weight: 600;

  &.disabled {
    opacity: 0.6;
  }
}

.demo-tip {
  text-align: center;
  font-size: 24rpx;
  color: #bbb;
  margin-top: 24rpx;
}
</style>
