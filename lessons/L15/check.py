"""Урок L15: проверка результата конвейера в хранилище. Запуск: python lessons/L15/check.py [батч]"""
import csv
import io
import json
import sys

import boto3

s3 = boto3.Session(profile_name="writer").client("s3")
BATCH = sys.argv[1] if len(sys.argv) > 1 else "2026-11-04"
EXPECTED = [("2026-11-01", "2", "1600"), ("2026-11-02", "2", "3400"), ("2026-11-03", "2", "1000")]


def get(key):
    return s3.get_object(Bucket="course-lake", Key=key)["Body"].read().decode()


problems = []
daily = [tuple(r.values()) for r in csv.DictReader(io.StringIO(get("curated/orders/daily_sales.csv")))]
if daily != EXPECTED:
    problems.append(f"итоги по дням: {[d[2] for d in daily]} ₽, ожидалось {[e[2] for e in EXPECTED]} ₽")
m = json.loads(get(f"catalog/orders_daily/batch={BATCH}/manifest.json"))
for field, want in (("accepted", 6), ("duplicates", 1), ("rejected", 1), ("total_rub", 6000)):
    if m[field] != want:
        problems.append(f"{field} = {m[field]}, ожидалось {want}")
rejected = list(csv.DictReader(io.StringIO(get(f"quarantine/orders/batch={BATCH}/rejected.csv"))))
if [r["order_id"] for r in rejected] != ["o005"]:
    problems.append(f"в карантине {[r['order_id'] for r in rejected]}, ожидалось ['o005']")

if problems:
    print("ПРОВЕРКА: ОШИБКА")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("ПРОВЕРКА: OK — 6 заказов, 1 повтор, 1 отбраковка, итого 6000 ₽")
