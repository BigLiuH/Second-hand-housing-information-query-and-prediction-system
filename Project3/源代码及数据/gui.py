import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Toplevel
from numpy import dtype
from openpyxl.styles.builtins import styles
from win32ui import types

# def loaddata():
#     citys=["沈阳", "北京", "上海", "深圳", "广州", "天津", "成都","南京","西安","重庆"]
#     file_path="房源.csv"
#     info= pd.DataFrame()
#     for city in citys:
#         with open(f"{city}.csv", "r", encoding="utf-8") as f:
#             data = pd.read_csv(f)
#             info = pd.concat([info, data], axis=0)
#     info.to_csv(file_path, index=False)
#     return info

# data=pd.read_csv("F:\\PyCharmProject\\PythonStudy\\Project2\\房源.csv",encoding="utf-8")

# 设置matplotlib使用的中文字体，避免警告
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或者 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义后端 API 的 URL
url = "http://127.0.0.1:8080/houses"


# 获取后端数据
try:
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    data = response.json()  # 解析 JSON 数据

    # 提取房源数据
    houses = data.get("houses", [])

    # 将房源数据转换为 pandas DataFrame
    data = pd.DataFrame(houses)

    # 确保列名一致
    data.columns = ["房屋信息链接", "房屋地址", "户型", "房屋面积", "朝向", "装修", "楼层", "年份", "房屋类型", "价格", "城市"]

    # 打印 DataFrame 内容（可以查看转换结果）
    print(data.head())

except requests.RequestException as e:
    print("请求后端数据失败:", e)
except Exception as e:
    print("处理数据时出错:", e)

# 创建主窗口
print(data.dtypes)
print(type(data))
root = tk.Tk()
root.title("二手房查询")
root.geometry("1200x800")


def open_sub_window():
    # 创建子窗口
    sub_window = Toplevel(root)
    sub_window.title("统计信息与条形图")
    sub_window.geometry("700x600")

    # 获取筛选后的数据
    filtered_data = filter_data()

    # 统计各个城市的房屋数量
    city_counts = filtered_data['城市'].value_counts()

    # 创建标签，显示房源数量
    label = tk.Label(sub_window, text="筛选后的房源数量：{}".format(len(filtered_data)))
    label.pack(pady=20)

    # 创建条形图
    fig, ax = plt.subplots(figsize=(6, 4))
    city_counts.plot(kind='bar', ax=ax, color='skyblue')

    ax.set_title('各城市房屋数量')
    ax.set_xlabel('城市')
    ax.set_ylabel('房屋数量')

    # 将Matplotlib图表嵌入到Tkinter窗口
    canvas = FigureCanvasTkAgg(fig, master=sub_window)  # 将图形嵌入到子窗口
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    # 添加关闭按钮
    close_button = tk.Button(sub_window, text="关闭", command=sub_window.destroy)
    close_button.pack(pady=10)
# 顶部搜索栏
top_frame = tk.Frame(root, bg="white", height=50)
top_frame.pack(side=tk.TOP, fill=tk.X)


search_label = tk.Label(top_frame, text="搜索房源：(输入小区名开始找房)", bg="white", font=("Arial", 12))
search_label.pack(side=tk.LEFT, padx=10, pady=10)

search_entry = tk.Entry(top_frame, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

search_button = tk.Button(top_frame, text="统计", bg="#0078d7", fg="white", font=("Arial", 12), command=open_sub_window)
search_button.pack(side=tk.RIGHT, padx=10)

# 筛选区域
citys_frame = tk.Frame(root, bg="#f7f7f7", height=50)
citys_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
citys_label = tk.Label(citys_frame, text="按城市筛选", bg="#f7f7f7")
citys_label.pack(side=tk.LEFT, padx=10)

roomstyle_frame = tk.Frame(root, bg="#f7f7f7", height=50)
roomstyle_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
roomstyle_label = tk.Label(roomstyle_frame, text="按户型筛选", bg="#f7f7f7")
roomstyle_label.pack(side=tk.LEFT, padx=10)

floor_frame = tk.Frame(root, bg="#f7f7f7", height=50)
floor_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
floor_label = tk.Label(floor_frame, text="按楼层筛选", bg="#f7f7f7")
floor_label.pack(side=tk.LEFT, padx=10)

decoration_frame = tk.Frame(root, bg="#f7f7f7", height=50)
decoration_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
decoration_label = tk.Label(decoration_frame, text="按装修筛选", bg="#f7f7f7")
decoration_label.pack(side=tk.LEFT, padx=10)

years_frame = tk.Frame(root, bg="#f7f7f7", height=50)
years_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
years_label = tk.Label(years_frame, text="按年份筛选", bg="#f7f7f7")
years_label.pack(side=tk.LEFT, padx=10)

building_type_frame = tk.Frame(root, bg="#f7f7f7", height=50)
building_type_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
building_type_label = tk.Label(building_type_frame, text="按房屋类型筛选", bg="#f7f7f7")
building_type_label.pack(side=tk.LEFT, padx=10)

price_frame = tk.Frame(root, bg="#f7f7f7", height=50)
price_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
price_label = tk.Label(price_frame, text="按价格筛选", bg="#f7f7f7")
price_label.pack(side=tk.LEFT, padx=10)

area_frame = tk.Frame(root, bg="#f7f7f7", height=50)
area_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
area_label = tk.Label(area_frame, text="按面积筛选", bg="#f7f7f7")
area_label.pack(side=tk.LEFT, padx=10)


# 筛选项
citys={
    "沈阳": {"label": "沈阳", "condition": lambda x: "沈阳" in x["城市"]},
    "北京": {"label": "北京", "condition": lambda x: "北京" in x["城市"]},
    "上海": {"label": "上海", "condition": lambda x: "上海" in x["城市"]},
    "深圳": {"label": "深圳", "condition": lambda x: "深圳" in x["城市"]},
    "广州": {"label": "广州", "condition": lambda x: "广州" in x["城市"]},
    "天津": {"label": "天津", "condition": lambda x: "天津" in x["城市"]},
    "成都": {"label": "成都", "condition": lambda x: "成都" in x["城市"]},
    "南京": {"label": "南京", "condition": lambda x: "南京" in x["城市"]},
    "西安": {"label": "西安", "condition": lambda x: "西安" in x["城市"]},
    "重庆": {"label": "重庆", "condition": lambda x: "重庆" in x["城市"]},
}
roomstyle={
    "1室":{ "label": "1室", "condition": lambda x: "1" in x["户型"]},
    "2室":{ "label": "2室", "condition": lambda x: "2" in x["户型"]},
    "3室":{ "label": "3室", "condition": lambda x: "3" in x["户型"]},
    "4室":{ "label": "4室", "condition": lambda x: "4" in x["户型"]},
    "5室":{ "label": "5室", "condition": lambda x: "5" in x["户型"]},
}
floor={
    "高楼层":{ "label": "高楼层", "condition": lambda x: "高" in x["楼层"]},
    "中楼层":{ "label": "中楼层", "condition": lambda x: "中" in x["楼层"]},
    "低楼层":{ "label": "低楼层", "condition": lambda x: "低" in x["楼层"]},
}
decoration={
    "毛坯":{ "label": "毛坯", "condition": lambda x: "毛坯" in x["装修"]},
    "简装":{ "label": "简装", "condition": lambda x: "简装" in x["装修"]},
    "精装":{ "label": "精装", "condition": lambda x: "精装" in x["装修"]},
}
years={
    "5年以内":{ "label": "5年以内", "condition": lambda x: int(x["年份"]) >= 2019},
    "5-10年":{ "label": "5-10年", "condition": lambda x: int(x["年份"]) >= 2014 and int(x["年代"]) < 2019},
    "10年以上":{ "label": "10年以上", "condition": lambda x: int(x["年份"]) < 2014},
}
building_types={
    "塔楼":{ "label": "塔楼", "condition": lambda x: "塔楼" in x["类型"]},
    "板楼":{ "label": "板楼", "condition": lambda x: "板楼" in x["类型"]},
    "板塔结合":{ "label": "板塔结合", "condition": lambda x: "板塔结合" in x["类型"]},
}
price={
    "50万以下":{ "label": "50万以下", "condition": lambda x: float(x["价格"]) < 50},
    "50-100万":{ "label": "50-100万", "condition": lambda x: float(x["价格"]) >= 50 and float(x["价格"]) < 100},
    "100-150万":{ "label": "100-150万", "condition": lambda x: float(x["价格"]) >= 100 and float(x["价格"]) < 150},
    "150-200万":{ "label": "150-200万", "condition": lambda x: float(x["价格"]) >= 150 and float(x["价格"]) < 200},
    "200万以上":{ "label": "200万以上", "condition": lambda x: float(x["价格"]) >= 200},
}
area={
    "50平米以下":{ "label": "50平米以下", "condition": lambda x: float(x["房屋面积"]) < 50},
    "50-100平米":{ "label": "50-100平米", "condition": lambda x: float(x["房屋面积"]) >= 50 and float(x["房屋面积"]) < 100},
    "100-150平米":{ "label": "100-150平米", "condition": lambda x: float(x["房屋面积"]) >= 100 and float(x["房屋面积"]) < 150},
    "150-200平米":{ "label": "150-200平米", "condition": lambda x: float(x["房屋面积"]) >= 150 and float(x["房屋面积"]) < 200},
    "200平米以上":{ "label": "200平米以上", "condition": lambda x: float(x["房屋面积"]) >= 200},
}

citys_vars = {key: tk.BooleanVar(value=False) for key in citys}
roomstyle_vars = {key: tk.BooleanVar(value=False) for key in roomstyle}
floor_vars = {key: tk.BooleanVar(value=False) for key in floor}
decoration_vars = {key: tk.BooleanVar(value=False) for key in decoration}
years_vars = {key: tk.BooleanVar(value=False) for key in years}
building_type_vars = {key: tk.BooleanVar(value=False) for key in building_types}
price_vars = {key: tk.BooleanVar(value=False) for key in price}
area_vars={key: tk.BooleanVar(value=False) for key in area}

for key, info in citys.items():
    chk = tk.Checkbutton(citys_frame, text=info["label"], variable=citys_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in roomstyle.items():
    chk = tk.Checkbutton(roomstyle_frame, text=info["label"], variable=roomstyle_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in floor.items():
    chk = tk.Checkbutton(floor_frame, text=info["label"], variable=floor_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in decoration.items():
    chk = tk.Checkbutton(decoration_frame, text=info["label"], variable=decoration_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in years.items():
    chk = tk.Checkbutton(years_frame, text=info["label"], variable=years_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in building_types.items():
    chk = tk.Checkbutton(building_type_frame, text=info["label"], variable=building_type_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in price.items():
    chk = tk.Checkbutton(price_frame, text=info["label"], variable=price_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

for key, info in area.items():
    chk = tk.Checkbutton(area_frame, text=info["label"], variable=area_vars[key], bg="#f7f7f7")
    chk.pack(side=tk.LEFT, padx=10)

# 更新表格显示
def update_table(filtered_data):
    # 清空现有的表格
    for item in tree.get_children():
        tree.delete(item)

    # 插入筛选后的数据到表格中
    for index, row in filtered_data.iterrows():
        tree.insert('', 'end', values=list(row))


# 筛选函数
def filter_data():
    # 获取选中的筛选条件
    selected_cities = [key for key, var in citys_vars.items() if var.get()]
    selected_roomstyles = [key for key, var in roomstyle_vars.items() if var.get()]
    selected_floors = [key for key, var in floor_vars.items() if var.get()]
    selected_decorations = [key for key, var in decoration_vars.items() if var.get()]
    selected_years = [key for key, var in years_vars.items() if var.get()]
    selected_building_types = [key for key, var in building_type_vars.items() if var.get()]
    selected_prices = [key for key, var in price_vars.items() if var.get()]
    selected_areas = [key for key, var in area_vars.items() if var.get()]
    # 根据选中的筛选条件进行数据过滤
    filtered_data = data
    if search_entry.get():
        # 模糊匹配小区名
        filtered_data = filtered_data[filtered_data['房屋地址'].str.contains(str(search_entry.get()), case=False, na=False)]
    if selected_cities:
        filtered_data = filtered_data[filtered_data['城市'].isin(selected_cities)]
    if selected_roomstyles:
        # 模糊匹配户型
        filtered_data = filtered_data[
            filtered_data['户型'].str.contains('|'.join(selected_roomstyles), case=False, na=False)]

    if selected_floors:
        # 模糊匹配楼层
        filtered_data = filtered_data[
            filtered_data['楼层'].str.contains('|'.join(selected_floors), case=False, na=False)]

    if selected_decorations:
        # 模糊匹配装修
        filtered_data = filtered_data[
            filtered_data['装修'].str.contains('|'.join(selected_decorations), case=False, na=False)]

    if selected_years:
        temp_data = pd.DataFrame()  # 用于存放筛选结果

        # 定义年份条件映射
        years_mapping = {
            "5年以内": lambda x: pd.to_numeric(x, errors='coerce') >= 2019,  # 转换为数字，无法转换的为 NaN
            "5-10年": lambda x: (2014 <= pd.to_numeric(x, errors='coerce') < 2019),  # 转换为数字，无法转换的为 NaN
            "10年以上": lambda x: pd.to_numeric(x, errors='coerce') < 2014  # 转换为数字，无法转换的为 NaN
        }

        # 获取筛选条件的函数
        selected_years_conditions = [years_mapping[year] for year in selected_years]

        origin_data = filtered_data  # 原始数据

        # 遍历所有条件并应用
        for condition in selected_years_conditions:
            # 应用条件筛选年份数据
            temp_filtered = origin_data[origin_data['年份'].apply(condition)]  # 仅保留符合条件的行
            temp_data = pd.concat([temp_data, temp_filtered], axis=0, ignore_index=True)  # 合并筛选后的数据

        filtered_data = temp_data  # 更新为最终的筛选结果

    if selected_building_types:
        # 模糊匹配房屋类型
        filtered_data = filtered_data[
            filtered_data['房屋类型'].str.contains('|'.join(selected_building_types), case=False, na=False)]

    if selected_prices:
        # 对价格字段进行数值筛选，去除单位并转换为数值
        price_mapping = {
            "50万以下": lambda x: float(x) < 50,
            "50-100万": lambda x: 50 <= float(x) < 100,
            "100-150万": lambda x: 100 <= float(x) < 150,
            "150-200万": lambda x: 150 <= float(x) < 200,
            "200万以上": lambda x: float(x) >= 200,
        }
        # 筛选价格区间
        temp_data = pd.DataFrame()
        origin_data=filtered_data
        selected_price_conditions = [price_mapping[price] for price in selected_prices]
        for condition in selected_price_conditions:
            filtered_data = origin_data[origin_data['价格'].apply(condition)]
            temp_data = pd.concat([temp_data, filtered_data], axis=0, ignore_index=True)
        filtered_data = temp_data
    if selected_areas:
        # 对面积字段进行数值筛选，去除单位并转换为数值
        area_mapping = {
            "50平米以下": lambda x: float(x) < 50,
            "50-100平米": lambda x: 50 <= float(x) < 100,
            "100-150平米": lambda x: 100 <= float(x) < 150,
            "150-200平米": lambda x: 150 <= float(x) < 200,
            "200平米以上": lambda x: float(x) >= 200,
        }
        # 筛选面积区间
        temp_data = pd.DataFrame()
        origin_data = filtered_data
        selected_area_conditions = [area_mapping[area] for area in selected_areas]
        for condition in selected_area_conditions:
            filtered_data = origin_data[origin_data['房屋面积'].apply(condition)]
            temp_data = pd.concat([temp_data, filtered_data], axis=0, ignore_index=True)
        filtered_data = temp_data
    # 更新表格显示
    update_table(filtered_data)
    return  filtered_data

# 筛选按钮
filter_button = tk.Button(top_frame, text="筛选", bg="#28a745", fg="white", font=("Arial", 12), command=filter_data)
filter_button.pack(side=tk.RIGHT, padx=10)

# 创建 Treeview 来展示数据
tree = ttk.Treeview(root, columns=list(data.columns), show="headings")

# 设置列标题
for col in data.columns:
    tree.heading(col, text=col, anchor=tk.CENTER)
for col in data.columns:
    tree.column(col, anchor=tk.CENTER, width=100)


# 插入数据到表格中
update_table(data)  # 初始化时显示所有数据

# 创建滚动条
scrollbar_y = tk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=tree.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(xscrollcommand=scrollbar_x.set)

tree.pack(expand=True, fill=tk.BOTH)

root.mainloop()