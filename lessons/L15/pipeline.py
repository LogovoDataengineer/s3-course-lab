"""Урок L15: конвейер raw → curated. Запуск: python lessons/L15/pipeline.py [батч]

Читает выгрузку заказов по манифесту из catalog/, вызывает transform_orders из transform.py
и публикует результат: curated/ — итоги по дням, quarantine/ — отбракованные строки,
catalog/ — манифест результата (пишется последним).
Этот файл менять не нужно: задание урока — функция transform_orders в transform.py.
"""
import csv
import hashlib
import io
import json
import sys

import boto3

from transform import transform_orders

s3 = boto3.Session(profile_name="writer").client("s3")
BUCKET = "course-lake"
BATCH = sys.argv[1] if len(sys.argv) > 1 else "2026-11-04"


def get(key):
    return s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()


def put(key, body, content_type):
    s3.put_object(Bucket=BUCKET, Key=key, Body=body, ContentType=content_type)
    return {"key": key, "sha256": hashlib.sha256(body).hexdigest()}


def to_csv(rows, fields):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode()


# 1. Вход: только файлы, перечисленные в манифесте, с проверкой контрольных сумм.
source = json.loads(get(f"catalog/orders/batch={BATCH}/manifest.json"))
rows = []
for item in source["files"]:
    body = get(item["key"])
    if hashlib.sha256(body).hexdigest() != item["sha256"]:
        sys.exit(f"Контрольная сумма не совпала: {item['key']}")
    rows += list(csv.DictReader(io.StringIO(body.decode())))
print(f"Прочитано строк: {len(rows)} из {len(source['files'])} файлов батча {BATCH}")

# 2. Преобразование — задание урока.
summary, stats = transform_orders(rows)

# 3. Выход: итоги, карантин, затем манифест результата.
outputs = [
    put("curated/orders/daily_sales.csv", to_csv(summary, ["event_date", "orders", "amount_rub"]), "text/csv"),
    put(f"quarantine/orders/batch={BATCH}/rejected.csv",
        to_csv(stats["rejected"], ["order_id", "event_date", "category", "amount_rub"]), "text/csv"),
]
manifest = {"dataset": "orders_daily", "source_batch": BATCH, "files": outputs,
            "accepted": stats["accepted"], "duplicates": stats["duplicates"], "rejected": len(stats["rejected"]),
            "total_rub": sum(day["amount_rub"] for day in summary)}
put(f"catalog/orders_daily/batch={BATCH}/manifest.json", json.dumps(manifest, indent=2).encode(), "application/json")
print(f"Принято: {stats['accepted']}, повторов: {stats['duplicates']}, отбраковано: {len(stats['rejected'])}")
print("Итоги по дням:", [(d["event_date"], d["orders"], d["amount_rub"]) for d in summary])
print("Опубликовано: curated/orders/daily_sales.csv и", f"catalog/orders_daily/batch={BATCH}/manifest.json")
