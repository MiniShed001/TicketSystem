/**
 * 后端接口定义
 */
import { get, post, patch } from '../utils/request.js'

export const api = {
  // ===== 活动 =====
  getEvents(params) {
    return get('/api/events/', params)
  },
  getEventDetail(id) {
    return get(`/api/events/${id}/`)
  },

  // ===== 用户 =====
  login(data) {
    return post('/api/users/login/', data)
  },
  register(data) {
    return post('/api/users/register/', data)
  },
  getUserInfo() {
    return get('/api/users/me/')
  },
  updateUserInfo(data) {
    return patch('/api/users/me/', data)
  },

  // ===== 订单 =====
  createOrder(data) {
    return post('/api/orders/', data)
  },
  getOrders(params) {
    return get('/api/orders/list/', params)
  },
  getOrderDetail(id) {
    return get(`/api/orders/${id}/`)
  },
  payOrder(id) {
    return post(`/api/orders/${id}/pay/`, {})
  },
  cancelOrder(id) {
    return post(`/api/orders/${id}/cancel/`, {})
  },
}
