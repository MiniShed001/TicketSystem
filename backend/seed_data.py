# -*- coding: utf-8 -*-
"""
演示数据初始化脚本
用法: python manage.py shell < seed_data.py
创建: 超级管理员 / 演示用户 / 演示活动(含封面图) / 场次 / 票档
"""
import os
import random
from datetime import timedelta
from io import BytesIO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tickets.settings")
import django

django.setup()

from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from apps.events.models import Event, Session, TicketType
from apps.users.models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media", "covers")
os.makedirs(MEDIA_DIR, exist_ok=True)


def make_cover(filename, title, subtitle, color1, color2):
    """生成一张渐变封面图"""
    img = Image.new("RGB", (800, 450))
    draw = ImageDraw.Draw(img)
    for y in range(450):
        ratio = y / 450
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (800, y)], fill=(r, g, b))
    # 装饰圆
    for i in range(6):
        x = random.randint(40, 760)
        y = random.randint(40, 410)
        radius = random.randint(20, 60)
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            outline=(255, 255, 255),
            width=2,
        )
    # 文字
    try:
        font_big = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 48)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
    except Exception:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    draw.text((40, 150), title, font=font_big, fill=(255, 255, 255))
    draw.text((40, 240), subtitle, font=font_small, fill=(235, 235, 235))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return ContentFile(buf.getvalue())


def main():
    # ---------- 用户 ----------
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123456", nickname="管理员")
        print("[OK] 超级管理员: admin / admin123456")
    else:
        print("[SKIP] admin 已存在")

    if not User.objects.filter(username="demo").exists():
        User.objects.create_user("demo", "demo@example.com", "demo123456", nickname="演示用户", phone="13800000000")
        print("[OK] 演示用户: demo / demo123456")
    else:
        print("[SKIP] demo 已存在")

    # ---------- 活动 ----------
    events_data = [
        {
            "title": "2026 城市之光跨年演唱会",
            "category": "concert",
            "venue": "贵阳奥体中心",
            "city": "贵阳",
            "address": "观山湖区奥体中心体育场",
            "description": "全城期待的年度音乐盛典，多位实力唱将倾情献唱，用音乐迎接新年的到来。现场配备顶级灯光舞美，带来沉浸式视听体验。",
            "days_offset": 10,
            "hot": True,
            "colors": ((64, 64, 200), (180, 60, 200)),
        },
        {
            "title": "话剧《半山听雨》全国巡演·贵阳站",
            "category": "drama",
            "venue": "贵阳大剧院",
            "city": "贵阳",
            "address": "云岩区中华中路贵阳大剧院",
            "description": "一部关于爱与成长的话剧，剧情细腻动人，演员阵容实力派班底，被誉为年度最值得一看的舞台作品。",
            "days_offset": 15,
            "hot": True,
            "colors": ((30, 90, 60), (60, 160, 120)),
        },
        {
            "title": "国潮动漫游戏展 · 2026 秋季场",
            "category": "exhibition",
            "venue": "贵阳国际会议展览中心",
            "city": "贵阳",
            "address": "观山湖区长岭北路 1 号",
            "description": "汇聚国内外知名动漫游戏 IP，现场有签售、Coser 巡游、新品首发、互动体验区，二次元爱好者的年度盛会。",
            "days_offset": 20,
            "hot": False,
            "colors": ((200, 90, 40), (240, 180, 60)),
        },
        {
            "title": "「夜莺与玫瑰」经典电影原声音乐会",
            "category": "concert",
            "venue": "贵阳音乐厅",
            "city": "贵阳",
            "address": "南明区遵义路 15 号贵阳音乐厅",
            "description": "交响乐团现场演奏经典电影原声配乐，配合大屏电影片段放映，重现银幕中的动人瞬间。",
            "days_offset": 25,
            "hot": False,
            "colors": ((70, 40, 140), (150, 90, 220)),
        },
        {
            "title": "CBA 季前赛：贵州主场对阵邀请赛",
            "category": "sports",
            "venue": "贵阳金阳体育馆",
            "city": "贵阳",
            "address": "观山湖区金阳南路金阳体育馆",
            "description": "职业篮球季前热身赛，近距离感受职业球员的精彩对决，现场氛围热烈。",
            "days_offset": 30,
            "hot": False,
            "colors": ((180, 60, 40), (240, 140, 60)),
        },
        {
            "title": "沉浸式光影艺术展「星河入梦」",
            "category": "exhibition",
            "venue": "贵阳当代美术馆",
            "city": "贵阳",
            "address": "南明区筑城广场当代美术馆",
            "description": "多感官沉浸式光影艺术展，用数字光影构建星河梦境，适合打卡拍照，亲子同游。",
            "days_offset": 35,
            "hot": False,
            "colors": ((20, 40, 120), (60, 160, 220)),
        },
    ]

    now = timezone.localtime()

    def evening(days):
        """第 N 天晚上 19:30 的本地时刻"""
        return (now + timedelta(days=days)).replace(hour=19, minute=30, second=0, microsecond=0)

    def night(days):
        """第 N 天晚上 22:00 的本地时刻"""
        return (now + timedelta(days=days)).replace(hour=22, minute=0, second=0, microsecond=0)
    for idx, ev in enumerate(events_data, start=1):
        if Event.objects.filter(title=ev["title"]).exists():
            print(f"[SKIP] 活动已存在: {ev['title']}")
            continue
        event = Event.objects.create(
            title=ev["title"],
            category=ev["category"],
            venue=ev["venue"],
            city=ev["city"],
            address=ev["address"],
            description=ev["description"],
            start_time=evening(ev["days_offset"]),
            end_time=night(ev["days_offset"]),
            status="on",
            is_hot=ev["hot"],
        )
        filename = f"cover_{idx}.jpg"
        cover_file = make_cover(filename, ev["title"], f"{ev['city']} · {ev['venue']}", ev["colors"][0], ev["colors"][1])
        event.cover.save(filename, cover_file, save=True)
        print(f"[OK] 活动: {ev['title']}")

        # 场次：主日场 + 次日晚场
        session1 = Session.objects.create(
            event=event,
            name=f"{ev['days_offset']}天后 19:30 场",
            start_time=event.start_time,
            end_time=event.end_time,
            status="open",
        )
        session2 = Session.objects.create(
            event=event,
            name=f"{ev['days_offset'] + 1}天后 19:30 场",
            start_time=evening(ev["days_offset"] + 1),
            end_time=night(ev["days_offset"] + 1),
            status="open",
        )
        # 票档
        ticket_defs = [
            ("普通票", 180, 500, "普通区域，先到先坐"),
            ("一等票", 380, 300, "前区舒适座位"),
            ("VIP 票", 680, 100, "VIP 专属区域，含纪念周边"),
        ]
        for tname, price, count, desc in ticket_defs:
            TicketType.objects.create(
                session=session1,
                name=tname,
                price=price,
                total_count=count,
                sold_count=random.randint(0, int(count * 0.6)),
                description=desc,
            )
            TicketType.objects.create(
                session=session2,
                name=tname,
                price=price,
                total_count=count,
                sold_count=random.randint(0, int(count * 0.4)),
                description=desc,
            )
        print(f"[OK] 场次与票档: {ev['title']} (2 场次 x 3 票档)")

    print("\n=== 演示数据初始化完成 ===")
    print(f"活动数量: {Event.objects.count()}")
    print(f"场次数量: {Session.objects.count()}")
    print(f"票档数量: {TicketType.objects.count()}")
    print(f"用户数量: {User.objects.count()}")


if __name__ == "__main__":
    main()
