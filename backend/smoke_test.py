# -*- coding: utf-8 -*-
"""
票务系统 API 全链路冒烟测试
用法: python smoke_test.py
覆盖: 活动列表 -> 活动详情 -> 登录 -> 下单 -> 支付 -> 订单列表 -> 验票核销
"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8000/api"


def req(method, path, data=None, token=None):
    url = BASE + path
    body = json.dumps(data).encode("utf-8") if data is not None else None
    r = urllib.request.Request(url, data=body, method=method)
    r.add_header("Content-Type", "application/json")
    if token:
        r.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def check(step, ok, extra=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {step}" + (f"  {extra}" if extra else ""))
    if not ok:
        sys.exit(1)


def main():
    # 1. 活动列表
    s, data = req("GET", "/events/")
    check("活动列表", s == 200 and data["code"] == 0 and len(data["data"]["results"]) > 0, f"共 {data['data']['count']} 个活动")

    # 2. 活动详情
    event_id = data["data"]["results"][0]["id"]
    s, detail = req("GET", f"/events/{event_id}/")
    sessions = detail["data"]["sessions"]
    check("活动详情", s == 200 and len(sessions) > 0, f"场次数 {len(sessions)}")
    tt = sessions[0]["ticket_types"][0]
    check("票档信息", tt["remain_count"] > 0, f"票档 {tt['name']} ¥{tt['price']} 余 {tt['remain_count']}")

    # 3. 登录 demo 用户
    s, login = req("POST", "/users/login/", {"username": "demo", "password": "demo123456"})
    check("用户登录", s == 200 and login["code"] == 0, login["data"]["user"]["username"])
    token = login["data"]["tokens"]["access"]

    # 4. 下单
    order_payload = {
        "session_id": sessions[0]["id"],
        "ticket_type_id": tt["id"],
        "quantity": 2,
        "remark": "冒烟测试订单",
    }
    s, order = req("POST", "/orders/", order_payload, token)
    check("创建订单", s == 201 and order["code"] == 0, f"{order['data']['order_no']} ¥{order['data']['amount']}")
    order_id = order["data"]["id"]

    # 5. 支付
    s, pay = req("POST", f"/orders/{order_id}/pay/", {}, token)
    check("订单支付", s == 200 and pay["data"]["status"] == "paid", f"验票码 {pay['data']['ticket_code']}")
    ticket_code = pay["data"]["ticket_code"]

    # 6. 订单列表
    s, orders = req("GET", "/orders/list/", None, token)
    check("订单列表", s == 200 and orders["code"] == 0 and len(orders["data"]["results"]) >= 1, f"{orders['data']['count']} 条订单")

    # 7. 验票核销（需 staff，用 admin 登录）
    s, admin_login = req("POST", "/users/login/", {"username": "admin", "password": "admin123456"})
    check("管理员登录", s == 200, "")
    admin_token = admin_login["data"]["tokens"]["access"]
    s, verify = req("POST", "/orders/verify/", {"ticket_code": ticket_code}, admin_token)
    check("验票核销", s == 200 and verify["code"] == 0, f"核销订单 {verify['data']['order_no']}")

    # 8. 重复核销应失败
    s, verify2 = req("POST", "/orders/verify/", {"ticket_code": ticket_code}, admin_token)
    check("重复核销拦截", s == 400, verify2.get("message", ""))

    # 9. 未登录下单应 401
    s, noauth = req("POST", "/orders/", order_payload)
    check("未登录拦截", s == 401)

    print("\n=== 全链路冒烟测试全部通过 ===")


if __name__ == "__main__":
    main()
