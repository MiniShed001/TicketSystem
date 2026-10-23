import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    uni(),
  ],
  server: {
    // 监听所有地址：127.0.0.1 / localhost / 局域网 IP 均可访问（默认只监听 ::1 IPv6 会导致浏览器连不上）
    host: '0.0.0.0',
    port: 5173,
  },
})
