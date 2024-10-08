from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

cluster = "mongodb://localhost:27017/database"
client = MongoClient(cluster)
data = client.my_database
searching_price = data.xe_cho_tot

'''
# Dữ liệu
data = {
    '2021': [{'Hyundai': 116}, {'VinFast': 71}, {'Mazda': 53}, {'Toyota': 176}, {'Mitsubishi': 90},
             {'Ford': 63}, {'Peugeot': 18}, {'Mercedes Benz': 90}, {'Audi': 1}, {'Honda': 45},
             {'LandRover': 3}, {'Kia': 98}, {'Suzuki': 25}, {'Volvo': 3}, {'BMW': 6}, {'Porsche': 4},
             {'Volkswagen': 3}, {'Lexus': 7}, {'Nissan': 6}, {'MG': 6}, {'Zotye': 1}, {'Isuzu': 1},
             {'Hãng khác': 1}],
    '2020': [{'Suzuki': 22}, {'Mazda': 66}, {'VinFast': 47}, {'Kia': 105}, {'MG': 5}, {'Mitsubishi': 63},
             {'Ford': 90}, {'Hyundai': 89}, {'Toyota': 179}, {'Honda': 46}, {'Mercedes Benz': 43},
             {'Peugeot': 12}, {'Nissan': 4}, {'Isuzu': 4}, {'BMW': 3}, {'Gaz': 1}, {'Porsche': 6},
             {'Volvo': 2}, {'Lexus': 6}, {'Hãng khác': 2}, {'Subaru': 1}, {'LandRover': 3}, {'Chevrolet': 1},
             {'Audi': 1}]
}

# Trích xuất dữ liệu
brands = list(data.keys())
brand_colors = ['#FF5733', '#33FF57']     #'#3357FF, '#FF33A6' Màu tương phản cho mỗi hãng

# Vị trí trục x cho mỗi hãng
x_pos = []
start = 0
width = 0.8  # Độ rộng cột

# Chuẩn bị dữ liệu vẽ biểu đồ
plt.figure(figsize=(15, 8))
for idx, brand in enumerate(brands):
    cars = data[brand]
    model_names = [list(car.keys())[0] for car in cars]
    model_values = [list(car.values())[0] for car in cars]

    # Tạo vị trí cho mỗi hãng, thêm khoảng cách giữa các hãng
    x = np.arange(start, start + len(cars))
    x_pos.extend(x)

    # Vẽ cột cho mỗi hãng với màu sắc tương ứng và chú thích
    plt.bar(x, model_values, width=width, color=brand_colors[idx], label=brand)

    # Thêm khoảng cách giữa các hãng
    start += len(cars) + 1

# Thêm nhãn số lượng xe trên các cột
for bar in plt.gca().patches:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=8)

# Thiết lập nhãn, tiêu đề và cỡ chữ
plt.xticks(x_pos, [list(car.keys())[0] for brand in data.values() for car in brand], rotation=90, fontsize=10)
plt.xlabel('Hãng xe', fontsize=12)
plt.ylabel('Số lượng xe', fontsize=12)
plt.title('Biểu đồ thể hiện số lượng xe sản xuất của mỗi hãng qua năm 2024, 2023, 2022', fontsize=14)

# Hiển thị chú thích cho hãng xe
plt.legend(title='Năm sản xuất', fontsize=10, title_fontsize=12)

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()
'''

'''
top5_year_value = ['2024', '2023', '2022', '2021', '2020']
# [{'2024': 903}, {'2023': 575}, {'2022': 1121}, {'2021': 887}, {'2020': 801}]
brand_year = []
for i in range(len(top5_year_value)):
    print(f"Năm sản xuất {top5_year_value[i]}:")
    documents = searching_price.find({"year_production": top5_year_value[i]})
    brand_arr = []
    for doc in documents:
        brand = doc["brand_car"]
        brand_arr.append(brand)
    print(f"Tổng số doc chứa các hãng xe được sản xuất của năm {top5_year_value[i]} là: {len(brand_arr)}")

    unique_brand = list(dict.fromkeys(brand_arr))
    print(unique_brand)
    brand_value = []
    total = 0
    for index in range(len(unique_brand)):
        value = searching_price.count_documents({"brand_car": unique_brand[index], "year_production": top5_year_value[i]})
        pair = {unique_brand[index]: value}
        brand_value.append(pair)
        total += value

    print(total)
    couple = {top5_year_value[i]: brand_value}
    brand_year.append(couple)

print(brand_year)
[
{'2024': [{'Mitsubishi': 78}, {'VinFast': 96}, {'Ford': 76}, {'Hyundai': 126}, {'Suzuki': 31}, 
           {'Subaru': 16}, {'Kia': 63}, {'Mercedes Benz': 14}, {'Peugeot': 19}, {'MG': 45}, {'Honda': 53},
           {'Toyota': 144}, {'Mazda': 47}, {'Lexus': 6}, {'Hãng khác': 3}, {'BMW': 23}, {'BYD': 19}, 
           {'Nissan': 3}, {'Haval': 4}, {'Volkswagen': 22}, {'Volvo': 7}, {'Mini': 2}, {'Acura': 1}, 
           {'Isuzu': 1}, {'LandRover': 2}, {'Skoda': 2}]}, 
{'2023': [{'Hyundai': 74}, {'Mitsubishi': 59}, {'Suzuki': 6}, {'BMW': 17}, {'Ford': 92}, {'Toyota': 73}, 
          {'MG': 16}, {'Mazda': 33}, {'VinFast': 25}, {'Haval': 10}, {'Honda': 36}, {'Mercedes Benz': 34},
          {'Nissan': 4}, {'Lexus': 9}, {'Volvo': 18}, {'Kia': 34}, {'Porsche': 4}, {'LandRover': 6}, 
          {'Subaru': 9}, {'Isuzu': 2}, {'Wuling': 1}, {'Peugeot': 4}, {'Audi': 2}, {'Volkswagen': 5}, 
          {'Hãng khác': 1}, {'Daewoo': 1}]},
{'2022': [{'Hyundai': 146}, {'Ford': 95}, {'Mitsubishi': 80}, {'VinFast': 78}, {'Honda': 50}, {'MG': 30},
          {'Toyota': 210}, {'Mercedes Benz': 83}, {'Lexus': 10}, {'LandRover': 5}, {'Volvo': 11}, 
          {'Mazda': 75}, {'Kia': 158}, {'Peugeot': 32}, {'Suzuki': 28}, {'Nissan': 5}, {'Hãng khác': 2}, 
          {'BMW': 11}, {'Porsche': 6}, {'Volkswagen': 2}, {'Audi': 1}, {'Subaru': 1}, {'Mini': 1}, 
          {'Isuzu': 1}]}, 
{'2021': [{'Hyundai': 116}, {'VinFast': 71}, {'Mazda': 53}, {'Toyota': 176}, {'Mitsubishi': 90}, 
          {'Ford': 63}, {'Peugeot': 18}, {'Mercedes Benz': 90}, {'Audi': 1}, {'Honda': 45}, 
          {'LandRover': 3}, {'Kia': 98}, {'Suzuki': 25}, {'Volvo': 3}, {'BMW': 6}, {'Porsche': 4}, 
          {'Volkswagen': 3}, {'Lexus': 7}, {'Nissan': 6}, {'MG': 6}, {'Zotye': 1}, {'Isuzu': 1}, 
          {'Hãng khác': 1}]}, 
{'2020': [{'Suzuki': 22}, {'Mazda': 66}, {'VinFast': 47}, {'Kia': 105}, {'MG': 5}, {'Mitsubishi': 63}, 
          {'Ford': 90}, {'Hyundai': 89}, {'Toyota': 179}, {'Honda': 46}, {'Mercedes Benz': 43}, 
          {'Peugeot': 12}, {'Nissan': 4}, {'Isuzu': 4}, {'BMW': 3}, {'Gaz': 1}, {'Porsche': 6}, 
          {'Volvo': 2}, {'Lexus': 6}, {'Hãng khác': 2}, {'Subaru': 1}, {'LandRover': 3}, {'Chevrolet': 1},
          {'Audi': 1}]}
]

'''

'''
    Biểu đố năm sản xuất
count = 0
year_arr = []
documents = searching_price.find()
for doc in documents:
    year = doc['year_production']
    year_arr.append(year)
    count += 1
print(count)
print(len(year_arr))

unique_year = list(dict.fromkeys(year_arr))
print(len(unique_year))
total = 0
year_value = []
myquery = {}
for i in range(len(unique_year)):
    myquery["year_production"] = unique_year[i]
    value = searching_price.count_documents(myquery)
    pair = {unique_year[i]: value}
    year_value.append(pair)
    total += value
print(total)
print(year_value)

# Hàm sắp xếp, xử lý các năm dạng chuỗi
def get_year_key(item):
    year = list(item.keys())[0]
    if year == 'trước năm 1980':
        return float('-inf')  # Đưa "trước năm 1980" về đầu nếu muốn, đổi thành float('inf') nếu muốn cuối
    return int(year)  # Chuyển năm thành số để sắp xếp

# Sắp xếp mảng
sorted_cars_by_year = sorted(year_value, key=get_year_key, reverse=True)
print(sorted_cars_by_year)
# [{'2024': 903}, {'2023': 575}, {'2022': 1121}, {'2021': 887}, {'2020': 801}, {'2019': 859}, {'2018': 681}, {'2017': 459}, {'2016': 560}, {'2015': 394}, {'2014': 262}, {'2013': 174}, {'2012': 135}, {'2011': 186}, {'2010': 227}, {'2009': 210}, {'2008': 196}, {'2007': 124}, {'2006': 60}, {'2005': 86}, {'2004': 79}, {'2003': 76}, {'2002': 27}, {'2001': 23}, {'2000': 20}, {'1999': 4}, {'1998': 7}, {'1997': 12}, {'1996': 13}, {'1995': 3}, {'1994': 4}, {'1993': 10}, {'1992': 6}, {'1991': 3}, {'1990': 4}, {'1989': 1}, {'1988': 3}, {'1987': 4}, {'1986': 2}, {'1983': 1}, {'trước năm 1980': 9}]

# Chuẩn bị dữ liệu để vẽ
years = [list(item.keys())[0] for item in sorted_cars_by_year]
values = [list(item.values())[0] for item in sorted_cars_by_year]

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
bars = plt.bar(years, values, color='skyblue')
plt.title('Biểu Đồ thể hiện Số Lượng Xe được sản xuất theo từng năm')
plt.xlabel('Năm sản xuất')
plt.ylabel('Số lượng xe')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Thêm số lượng phía trên mỗi cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

# Hiện biểu đồ
plt.tight_layout()
plt.show()
'''

'''
# Dữ liệu
data = {
    'Honda': [{'Brio': 23}, {'City': 128}, {'CR V': 134}, {'Civic': 100}, {'BR-V': 13}, {'HR-V': 29},
              {'Jazz': 6}, {'Odyssey': 5}, {'Accord': 14}, {'Pilot': 1}, {'Dòng khác': 1}],
    'VinFast': [{'Lux SA2.0': 47}, {'Lux A2.0': 68}, {'VF3': 15}, {'VF6': 14}, {'Fadil': 93}, {'VF9': 24},
                {'VF7': 10}, {'VFe34': 13}, {'VF8': 25}, {'VF5': 25}, {'VF8 Lux': 6}, {'Dòng khác': 2},
                {'VF5 Plus': 10}],
    'Chevrolet': [{'Cruze': 48}, {'Camaro': 2}, {'Spark': 91}, {'Trailblazer': 8}, {'Captiva': 43},
                  {'Aveo': 25}, {'Lacetti': 7}, {'Orlando': 9}, {'Vivant': 5}, {'Colorado': 31}, {'Trax': 1},
                  {'Matiz': 2}, {'Dòng khác': 1}]
}

# Trích xuất dữ liệu
brands = list(data.keys())
brand_colors = ['#FF5733', '#33FF57', '#3357FF']     # '#FF33A6' Màu tương phản cho mỗi hãng

# Vị trí trục x cho mỗi hãng
x_pos = []
start = 0
width = 0.8  # Độ rộng cột

# Chuẩn bị dữ liệu vẽ biểu đồ
plt.figure(figsize=(15, 8))
for idx, brand in enumerate(brands):
    cars = data[brand]
    model_names = [list(car.keys())[0] for car in cars]
    model_values = [list(car.values())[0] for car in cars]

    # Tạo vị trí cho mỗi hãng, thêm khoảng cách giữa các hãng
    x = np.arange(start, start + len(cars))
    x_pos.extend(x)

    # Vẽ cột cho mỗi hãng với màu sắc tương ứng và chú thích
    plt.bar(x, model_values, width=width, color=brand_colors[idx], label=brand)

    # Thêm khoảng cách giữa các hãng
    start += len(cars) + 1

# Thêm nhãn số lượng xe trên các cột
for bar in plt.gca().patches:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=8)

# Thiết lập nhãn, tiêu đề và cỡ chữ
plt.xticks(x_pos, [list(car.keys())[0] for brand in data.values() for car in brand], rotation=90, fontsize=10)
plt.xlabel('Dòng xe', fontsize=12)
plt.ylabel('Số lượng xe', fontsize=12)
plt.title('Biểu đồ thể hiện số lượng xe của từng dòng xe', fontsize=14)

# Hiển thị chú thích cho hãng xe
plt.legend(title='Brand', fontsize=10, title_fontsize=12)

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()
'''

'''
brand = ['Toyota', 'Hyundai', 'Ford', 'Kia', 'Mercedes Benz', 'Mazda', 'Mitsubishi', 'Honda',
         'VinFast', 'Chevrolet']
brand_model = []
for i in range(len(brand)):
    print(f"Hãng xe {brand[i]}:")
    documents = searching_price.find({"brand_car": brand[i]})
    model_arr = []
    for doc in documents:
        model = doc["model_car"]
        model_arr.append(model)
    print(f"Tổng số doc chứa các dòng xe của hãng {brand[i]} là: {len(model_arr)}")

    unique_model = list(dict.fromkeys(model_arr))
    print(unique_model)
    model_value = []
    total = 0
    for index in range(len(unique_model)):
        value = searching_price.count_documents({"brand_car": brand[i], "model_car": unique_model[index]})
        pair = {unique_model[index]: value}
        model_value.append(pair)
        total += value

    print(total)
    couple = {brand[i]: model_value}
    brand_model.append(couple)

print(brand_model)

# [
{'Toyota': [{'Fortuner': 285}, {'Camry': 196}, {'Vios': 359}, {'Prius': 1}, {'Veloz Cross': 62}, 
               {'Corolla Cross': 86}, {'Innova': 425}, {'Wigo': 67}, {'Rush': 21}, {'Corolla Altis': 91}, 
               {'Corolla': 11}, {'Avanza Premio': 34}, {'Hiace': 23}, {'Innova Cross': 14}, {'Hilux': 31}, 
               {'Yaris': 52}, {'Raize': 47}, {'RAV4': 2}, {'Highlander': 1}, {'Alphard': 9}, 
               {'Land Cruiser': 24}, {'1116': 10}, {'Dòng khác': 7}, {'Crown': 6}, {'Zace': 22},
               {'Yaris Cross': 16}, {'Land Cruiser Prado': 25}, {'Sienna': 11}, {'Venza': 10}, {'IQ': 1}, 
               {'Prado': 14}, {'Cressida': 2}, {'Avalon': 2}, {'4 Runner': 1}, {'Aygo': 1}, {'Previa': 2}, 
               {'Corona': 1}]}, 
{'Hyundai': [{'Accent': 260}, {'Elantra': 86}, {'Grand i10': 207}, {'Tucson': 91}, {'Eon': 3}, 
             {'Starex': 8}, {'Stargazer': 20}, {'Creta': 42}, {'Genesis': 9}, {'Santa Fe': 162}, 
             {'i20': 18}, {'Avante': 14}, {'Kona': 34}, {'Sonata': 9}, {'Palisade': 12}, {'Venue': 6}, 
             {'Solati': 17}, {'Getz': 13}, {'i30': 5}, {'Grand Starex': 13}, {'Custin': 14}, 
             {'Mighty': 1}, {'Dòng khác': 6}, {'Verna': 5}, {'Veloster': 2}, {'County': 1}, 
             {'Galloper': 1}, {'Click': 2}, {'Universe': 1}, {'Veracruz': 1}, {'Azera': 1}]}, 
{'Ford': [{'Everest': 211}, {'EcoSport': 109}, {'Tourneo': 10}, {'Ranger': 342}, {'Focus': 64}, 
        {'Transit': 121}, {'Explorer': 16}, {'Territory': 33}, {'Mondeo': 11}, {'Mustang': 3}, 
        {'Escape': 33}, {'Fiesta': 34}, {'Laser': 14}, {'Dòng khác': 4}, {'Escort': 1}, {'F 150': 1}]}, 
{'Kia': [{'Morning': 215}, {'Rondo': 25}, {'Forte': 13}, {'Cerato': 88}, {'Carnival': 117}, 
         {'Sorento': 83}, {'Sonet': 37}, {'K3': 58}, {'Rio': 30}, {'Optima': 10}, {'Sedona': 99}, 
         {'Seltos': 47}, {'Carens': 44}, {'Sportage': 8}, {'K5': 11}, {'Cerato Koup': 2}, {'Soluto': 40}, 
         {'Spectra': 4}, {'CD5': 4}, {'Dòng khác': 6}, {'Picanto': 1}, {'Ray': 1}, {'Pride': 1}, 
         {'Soul': 2}]}, 
{'Mercedes Benz': [{'GLC': 109}, {'CLA Class': 13}, {'C Class': 179}, {'Vito': 2}, {'GLC Class': 73}, 
                   {'E Class': 98}, {'S Class': 44}, {'Sprinter': 13}, {'GLE Class': 14}, 
                   {'GLK Class': 13}, {'CLS Class': 1}, {'Dòng khác': 5}, {'GLB': 5}, {'Maybach': 6}, 
                   {'V Class': 5}, {'R Class': 3}, {'M Class': 1}, {'GLS Class': 16}, {'GLA Class': 9}, 
                   {'GL Class': 8}, {'ML Class': 4}, {'AMG': 5}, {'MB': 3}, {'CLK Class': 1}, 
                   {'EQE SUV': 1}, {'G Class': 7}, {'A Class': 3}, {'SL Class': 1}, {'GT Coupe': 2}, 
                   {'SLR Mclaren': 1}, {'CL Class': 1}]}, 
{'Mazda': [{'6': 62}, {'CX 5': 162}, {'CX 8': 51}, {'3': 215}, {'BT 50': 30}, {'CX 3': 12}, {'5': 1}, 
           {'2': 45}, {'323': 11}, {'Dòng khác': 2}, {'929': 1}, {'626': 4}, {'CX-30': 11}, {'Premacy': 2}, 
           {'CX 9': 1}, {'MPV': 1}]}, 
{'Mitsubishi': [{'Xpander': 215}, {'Outlander': 53}, {'Xpander Cross': 41}, {'Triton': 43}, 
                {'Grandis': 14}, {'Pajero Sport': 26}, {'Pajero': 18}, {'Xforce': 25}, {'Attrage': 74}, 
                {'Jolie': 41}, {'Dòng khác': 3}, {'Mirage': 4}, {'Lancer': 6}, {'Zinger': 5}, 
                {'Outlander Sport': 1}, {'3000GT': 1}]}, 
{'Honda': [{'Brio': 23}, {'City': 128}, {'CR V': 134}, {'Civic': 100}, {'BR-V': 13}, {'HR-V': 29}, 
           {'Jazz': 6}, {'Odyssey': 5}, {'Accord': 14}, {'Pilot': 1}, {'Dòng khác': 1}]}, 
{'VinFast': [{'Lux SA2.0': 47}, {'Lux A2.0': 68}, {'VF3': 15}, {'VF6': 14}, {'Fadil': 93}, {'VF9': 24}, 
            {'VF7': 10}, {'VFe34': 13}, {'VF8': 25}, {'VF5': 25}, {'VF8 Lux': 6}, {'Dòng khác': 2}, 
            {'VF5 Plus': 10}]}, 
{'Chevrolet': [{'Cruze': 48}, {'Camaro': 2}, {'Spark': 91}, {'Trailblazer': 8}, {'Captiva': 43}, 
               {'Aveo': 25}, {'Lacetti': 7}, {'Orlando': 9}, {'Vivant': 5}, {'Colorado': 31}, {'Trax': 1},
               {'Matiz': 2}, {'Dòng khác': 1}]}
]
'''

'''
{'Toyota': 1972} {'Hyundai': 1064} {'Ford': 1007} {'Kia': 946} {'Mercedes Benz': 646} {'Mazda': 611}
{'Mitsubishi': 570} {'Honda': 454} {'VinFast': 352} {'Chevrolet': 273} {'BMW': 160} {'Suzuki': 157} 
{'Lexus': 121} {'Peugeot': 118} {'Nissan': 104} {'MG': 102} {'Daewoo': 80} {'LandRover': 53} 
{'Volkswagen': 50} {'Porsche': 45} {'Isuzu': 44} {'Audi': 43} {'Volvo': 43} {'Hãng khác': 33} 
{'Subaru': 32} {'BYD': 23} {'Haval': 14} {'Mini': 13} {'Ssangyong': 7} {'Cadillac': 7} {'Daihatsu': 5} 
{'Jeep': 5} {'Jaguar': 5} {'Acura': 5} {'Bentley': 4} {'Lifan': 4} {'Fiat': 3} {'Luxgen': 3} {'Haima': 2}
{'Lamborghini': 2} {'Smart': 2} {'Changan': 2} {'Chrysler': 2} {'Proton': 2} {'Wuling': 2} {'Zotye': 2}
{'Skoda': 2} {'Asia': 1} {'Hummer': 1} {'UAZ': 1} {'Gaz': 1} {'Citroen': 1} {'Mekong': 1} {'Maybach': 1}
{'SYM': 1} {'Rover': 1} {'Infiniti': 1} {'Ferrari': 1} {'Dodge': 1} {'Baic': 1} {'Chery': 1} 
{'Maserati': 1}
        # BIỂU ĐỒ THỂ HIỆN SỐ LƯỢNG XE CỦA MỖI HÃNG
'''
count = 0
brand_arr = []
documents = searching_price.find()
for doc in documents:
    brand = doc['brand_car']
    brand_arr.append(brand)
    count += 1
print(count)
print(len(brand_arr))

unique_brand = list(dict.fromkeys(brand_arr))
print(len(unique_brand))
total = 0
brand_value = []
myquery = {}
for i in range(len(unique_brand)):
    myquery["brand_car"] = unique_brand[i]
    value = searching_price.count_documents(myquery)
    pair = {unique_brand[i]: value}
    brand_value.append(pair)
    total += value
print(total)

# Sắp xếp brand_value theo thứ tự giảm dần dựa trên số lượng xe
sorted_brand_value = sorted(brand_value, key=lambda x: list(x.values())[0], reverse=True)

# In kết quả đã sắp xếp
for brand in sorted_brand_value:
    print(brand)
top10_brand_value = sorted_brand_value[30:]
print(top10_brand_value)

# Extract brand names and values
brands = [list(item.keys())[0] for item in top10_brand_value]
values = [list(item.values())[0] for item in top10_brand_value]

# Create the bar chart
plt.figure(figsize=(15, 8))
bars = plt.bar(brands, values)

# Add the values on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=14)

# Set labels and title
plt.xticks(rotation=90)  # Rotate brand names for better readability
plt.xlabel('Hãng xe')
plt.ylabel('Số lượng xe')
plt.title('Biểu đồ thể hiện top32 hãng có số lượng đăng tải ít nhất')

# Display the chart
plt.tight_layout()
plt.show()
