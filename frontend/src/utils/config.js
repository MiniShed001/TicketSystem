/**
 * 全局配置
 * BASE_URL: 后端接口地址
 *
 * H5 端：默认 http://127.0.0.1:8000
 * 小程序 / App 端：
 *   - 微信开发者工具模拟器：可用 http://127.0.0.1:8000（需勾选"不校验合法域名"）
 *   - 真机调试：改为电脑局域网 IP，如 http://192.168.1.100:8000（手机与电脑同一 Wi-Fi）
 *   - 上线发布：必须改为已备案的 https 合法域名（如 https://api.example.com）
 */
// #ifdef H5
export const BASE_URL = 'http://127.0.0.1:8000'
// #endif

// #ifndef H5
// 小程序 / App 端：
//   - 模拟器调试：用 127.0.0.1（即电脑本机），后端默认启动即可连通
//   - 真机预览：改为电脑局域网 IP，如 http://192.168.2.138:8000（手机与电脑同一 Wi-Fi，
//     且后端需用 0.0.0.0 启动：python manage.py runserver 0.0.0.0:8000）
//   - 上线发布：必须改为已备案的 https 合法域名（如 https://api.example.com）
export const BASE_URL = 'http://127.0.0.1:8000'
// #endif

export const IMG_BASE = BASE_URL
