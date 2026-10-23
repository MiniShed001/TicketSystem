# 🎫 票务系统（Django + Uni-app）

一个前后端分离的在线票务系统：后端使用 **Django + DRF + JWT**，前端使用 **Uni-app（Vue3 + Vite）**，一套前端代码可编译到 H5 / 微信小程序 / App。

## 项目结构

```
D:\TicketSystem\
├── backend\                  # Django 后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── seed_data.py          # 演示数据初始化脚本
│   ├── smoke_test.py         # 后端 API 全链路冒烟测试
│   ├── tickets\              # 项目配置（settings/urls/分页）
│   ├── apps\
│   │   ├── users\            # 用户：注册/登录/资料（JWT）
│   │   ├── events\           # 活动：活动/场次/票档
│   │   └── orders\           # 订单：下单/支付/取消/验票核销
│   └── media\                # 上传图片（活动封面等）
├── frontend\                 # Uni-app 前端（Vue3 + Vite + pinia 式状态）
│   └── src\
│       ├── pages\            # 首页/详情/确认订单/订单列表/订单详情/登录/我的
│       ├── api\              # 接口定义
│       ├── utils\            # 请求封装/全局配置
│       └── store\            # 用户登录态（本地持久化）
├── docs\                     # 文档与页面效果截图
└── README.md
```

## 环境要求

| 组件 | 版本 |
|------|------|
| Python | 3.10+（本机验证 3.13） |
| Node.js | 18+（本机验证 22） |
| 数据库 | SQLite（默认，零配置）/ 可切换 MySQL |

## 一、启动后端（Django）

> 项目使用独立虚拟环境 `.venv`（位于 `backend\.venv`），不依赖系统 Python，双击 bat 或以下命令均可直接运行。

```powershell
cd D:\TicketSystem\backend

# 1.（仅首次）创建虚拟环境并安装依赖
D:\pythonDownLoad\python.exe -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2.（仅首次）初始化数据库（生成表结构）
.venv\Scripts\python.exe manage.py migrate

# 3.（仅首次）写入演示数据（管理员 + 演示用户 + 6 个活动/12 场次/36 票档）
.venv\Scripts\python.exe seed_data.py

# 4. 启动服务（0.0.0.0 监听，本机与局域网均可访问）
.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

或直接双击 **`D:\TicketSystem\start_backend.bat`**（已内置 venv，一键启动）。

**演示账号**

| 账号 | 密码 | 角色 |
|------|------|------|
| admin | admin123456 | 超级管理员（可进后台 http://127.0.0.1:8000/admin/，可验票核销） |
| demo | demo123456 | 普通用户（购票） |

**接口自测（可选）**

```powershell
python smoke_test.py        # 需先启动服务，覆盖 登录→下单→支付→验票 全链路
```

## 二、启动前端（Uni-app）

```powershell
cd D:\TicketSystem\frontend

# 1. 安装依赖
npm install

# 2. H5 开发模式（默认 http://localhost:5173）
npm run dev:h5

# 3. 构建 H5 生产包（输出 dist/build/h5）
npm run build:h5
```

浏览器打开 **http://localhost:5173** 即可使用完整购票流程。

**编译到小程序 / App**（需安装对应平台工具链）：

```powershell
npm run dev:mp-weixin      # 微信小程序（watch 模式，产物 dist\dev\mp-weixin，改代码自动编译）
npm run build:mp-weixin    # 微信小程序（生产构建，产物 dist\build\mp-weixin）
npm run dev:app            # App（HBuilderX 云打包）
```

### 微信开发者工具预览步骤（本地调试）

1. 下载安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)（稳定版即可）
2. 打开开发者工具 → 导入项目 → 目录选择 **`D:\TicketSystem\frontend\dist\dev\mp-weixin`**
3. AppID 使用**测试号**（工具会自动识别，project.config.json 已默认 touristappid），有正式小程序账号可填入 manifest.json 的 `mp-weixin.appid` 后重新编译
4. 右上角「详情」→「本地设置」→ 勾选 **不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书**（本地联调必需）
5. 模拟器即可预览完整购票流程；后端需保持运行（`python manage.py runserver 127.0.0.1:8000`）

**真机预览**：手机与电脑连同一 Wi-Fi，把 `frontend/src/utils/config.js` 中 `BASE_URL` 改为电脑局域网 IP（如 `http://192.168.1.100:8000`）后重新编译，点击「预览」扫码。**上线发布**必须将 `BASE_URL` 换成已备案的 https 合法域名。

## 三、功能清单

**用户端**
- 活动列表：分类筛选 / 关键词搜索 / 热门推荐 / 下拉刷新 / 上拉加载更多
- 活动详情：多场次选择、多票档选择（实时余票）、购票数量
- 下单支付：订单确认（含备注）、模拟支付、订单取消（释放库存）
- 电子票：支付成功后生成 8 位验票码，可复制
- 订单管理：全部/待支付/已支付/已使用/已取消 状态筛选
- 账号：注册 / 登录（JWT）/ 退出

**管理端（Django admin）**
- 活动 / 场次 / 票档的增删改查与余票管理
- 订单查看与状态管理
- 验票核销接口 `POST /api/orders/verify/`（需管理员 token）

## 四、核心 API

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | /api/users/register/ | 注册（成功即登录） | 否 |
| POST | /api/users/login/ | 登录拿 JWT | 否 |
| GET/PATCH | /api/users/me/ | 获取/修改个人资料 | 是 |
| GET | /api/events/ | 活动列表（category/q/hot/分页） | 否 |
| GET | /api/events/{id}/ | 活动详情（含场次票档） | 否 |
| POST | /api/orders/ | 创建订单（事务+行锁防超卖） | 是 |
| GET | /api/orders/list/ | 我的订单（status 筛选） | 是 |
| GET | /api/orders/{id}/ | 订单详情 | 是 |
| POST | /api/orders/{id}/pay/ | 模拟支付（生成验票码） | 是 |
| POST | /api/orders/{id}/cancel/ | 取消订单（归还库存） | 是 |
| POST | /api/orders/verify/ | 验票核销（防重复核销） | 管理员 |

统一响应格式：`{ "code": 0, "message": "ok", "data": ... }`，分页数据：`data: { count, next, previous, results }`。

## 五、前后端联调说明

- 前端默认请求 `http://127.0.0.1:8000`（见 `frontend/src/utils/config.js` 的 `BASE_URL`）。
- 后端已放开 CORS（开发环境），H5 跨域直接可用。
- **微信小程序**：需在 `manifest.json` 配置 appid，且 `BASE_URL` 必须是已备案的 https 合法域名；本地开发可勾选"不校验合法域名"。
- **App**：`BASE_URL` 改为局域网 IP 或线上地址，如 `http://192.168.x.x:8000`。

## 六、切换 MySQL（可选）

默认使用 SQLite（零配置）。切换 MySQL：

1. 安装驱动：`python -m pip install mysqlclient`（或 `pymysql`）
2. 修改 `backend/tickets/settings.py` 中 DATABASES 配置（文件内有注释示例），创建数据库 `ticket_db`（utf8mb4）
3. 重新 `python manage.py migrate`

## 七、注意事项

- 本项目为**模拟支付**（点击即支付成功），接入真实支付（微信/支付宝）时替换 `apps/orders/views.py` 中 `OrderPayView` 即可。
- 超时未支付订单暂未做自动取消任务，可在管理后台手动取消；如需自动释放可加定时任务（如 Celery beat）扫描 pending 订单。
- 生产部署时请修改 `settings.py` 中的 `SECRET_KEY`、关闭 `DEBUG`、收紧 `ALLOWED_HOSTS` 与 CORS 白名单。
- 活动封面图在 `seed_data.py` 中用 Pillow 自动生成，替换真实图片请上传到 Django admin 活动编辑页。
