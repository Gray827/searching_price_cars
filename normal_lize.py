import re
from pymongo import MongoClient

# Document từ MongoDB
cluster = "mongodb://localhost:27017/"
client = MongoClient(cluster)
data = client.demo_database
searching_price = data.searching_price_car

# 1. Chuẩn hóa price
def clean_price(price_str):
    # Tạo biến lưu giá trị tổng giá trị tiền
    total_price = 0

    # Tìm số "tỷ" (nếu có)
    ty_match = re.search(r'(\d+)\s*Tỷ', price_str)
    if ty_match:
        total_price += int(ty_match.group(1)) * 1000000000  # Nhân với 1 tỷ

    # Tìm số "triệu" (nếu có)
    trieu_match = re.search(r'(\d+)\s*Triệu', price_str)
    if trieu_match:
        total_price += int(trieu_match.group(1)) * 1000000  # Nhân với 1 triệu

    return total_price


# 2. Chuẩn hóa year_production
def clean_year(year_str):
    return int(year_str)

# 3. Chuẩn hóa kilometer
def clean_kilometer(kilometer_str):
    # Loại bỏ dấu phẩy và chữ "Km"
    kilometer_cleaned = re.sub(r'[^\d]', '', kilometer_str)
    return int(kilometer_cleaned)

# Áp dụng chuẩn hóa
for document in searching_price.find():
    price = document["price"]
    year = document["year_production"]
    kilometer = document["kilometer"]

    query_update = [
        ({"price": price}, {"$set": {"price": clean_price(price_str=price)}}),
        ({}, {"$set": {"currency": "VND"}}),
        ({"year_production": year}, {"$set": {"year_production": clean_year(year_str=year)}}),
        ({"kilometer": kilometer}, {"$set": {"kilometer": clean_kilometer(kilometer_str=kilometer)}})
    ]

    for query_filter, update_operation in query_update:
        result = searching_price.update_many(query_filter, update_operation, upsert=True)
