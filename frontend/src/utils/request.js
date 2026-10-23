/**
 * 请求封装：自动携带 JWT、统一错误处理、401 跳登录
 */
import userStore from '../store/user.js'
import { BASE_URL } from './config.js'

function toast(title) {
  uni.showToast({ title, icon: 'none' })
}

function toLogin() {
  setTimeout(() => {
    uni.navigateTo({ url: '/pages/login/login' })
  }, 600)
}

function request(options) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      timeout: 15000,
      header: {
        'Content-Type': 'application/json',
        ...(userStore.token ? { Authorization: 'Bearer ' + userStore.token } : {}),
        ...(options.header || {}),
      },
      success: (res) => {
        const body = res.data
        if (res.statusCode === 200 || res.statusCode === 201) {
          if (body && body.code === 0) {
            resolve(body)
          } else {
            toast((body && body.message) || '请求失败')
            reject(body)
          }
        } else if (res.statusCode === 401) {
          userStore.logout()
          toast('登录已过期，请重新登录')
          toLogin()
          reject(body)
        } else {
          toast((body && body.message) || `请求失败(${res.statusCode})`)
          reject(body)
        }
      },
      fail: (err) => {
        toast('网络异常，请确认后端服务已启动')
        reject(err)
      },
    })
  })
}

export function get(url, data) {
  return request({ url, method: 'GET', data })
}

export function post(url, data) {
  return request({ url, method: 'POST', data })
}

export function patch(url, data) {
  return request({ url, method: 'PATCH', data })
}

export default request
