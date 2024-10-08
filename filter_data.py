from pymongo import MongoClient

# Connect Mongodb
cluster = "mongodb://localhost:27017/database"
client = MongoClient(cluster)
data = client.my_database
searching_price = data.carmudi

count = 0
id_arr = []
documents = searching_price.find()
for doc in documents:
    id = doc["article_id"]
    id_arr.append(id)
    count += 1

unique_id = list(dict.fromkeys(id_arr))
print(len(unique_id))
print(f"Dữ liệu trong mongo: {count}")

# myquery = {}
# arr2 = []
# for i in range(len(unique_id)):
#     myquery["article_id"] = unique_id[i]
#     value = searching_price.count_documents(myquery)
#     print(f"ID {unique_id[i]}: {value}")
#     if value == 2:
#         arr2.append(unique_id[i])
#
# print(arr2)
# print(len(arr2))
# delete_query = {}
# for i in range(len(arr2)):
#     delete_query["article_id"] = arr2[i]
#     result = searching_price.delete_one(delete_query)