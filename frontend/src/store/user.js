/**
 * 轻量全局用户状态（响应式 + uni storage 持久化）
 */
import { reactive } from 'vue'

const TOKEN_KEY = 'ticket_token'
const REFRESH_KEY = 'ticket_refresh'
const USER_KEY = 'ticket_user'

const userStore = reactive({
  token: '',
  refreshToken: '',
  userInfo: null,
  isLogin: false,

  init() {
    this.token = uni.getStorageSync(TOKEN_KEY) || ''
    this.refreshToken = uni.getStorageSync(REFRESH_KEY) || ''
    this.userInfo = uni.getStorageSync(USER_KEY) || null
    this.isLogin = !!this.token
  },

  setLogin(tokens, userInfo) {
    this.token = tokens.access
    this.refreshToken = tokens.refresh
    this.userInfo = userInfo
    this.isLogin = true
    uni.setStorageSync(TOKEN_KEY, this.token)
    uni.setStorageSync(REFRESH_KEY, this.refreshToken)
    uni.setStorageSync(USER_KEY, this.userInfo)
  },

  setUserInfo(userInfo) {
    this.userInfo = userInfo
    uni.setStorageSync(USER_KEY, userInfo)
  },

  logout() {
    this.token = ''
    this.refreshToken = ''
    this.userInfo = null
    this.isLogin = false
    uni.removeStorageSync(TOKEN_KEY)
    uni.removeStorageSync(REFRESH_KEY)
    uni.removeStorageSync(USER_KEY)
  },
})

export default userStore
