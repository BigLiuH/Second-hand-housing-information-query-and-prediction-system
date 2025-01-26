import tkinter as tk
from tkinter import messagebox
import pickle
import pandas as pd
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# 加载编码对照表
with open('encoding_mappings.json', 'r', encoding='utf-8') as f:
    encoding_dict = json.load(f)

# 加载训练好的模型
# with open('house_price_model.pkl', 'rb') as f:
#     model = pickle.load(f)

# 训练时使用的特征名称顺序
columns = ['房屋区域', '室', '厅', '房屋面积', '装修', '楼层', '年份', '房屋类型', '县区']


# 创建GUI应用
class HousePricePredictor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("房屋价格预测系统")
        self.geometry("1000x750")  # 调整界面尺寸以容纳更多控件

        # 默认模型为随机森林
        self.selected_model = "RandomForest"

        # 输入框标签
        self.create_widgets()

    def create_widgets(self):
        # 居中显示
        self.label_title = tk.Label(self, text="请输入房屋信息", font=("Arial", 14))
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # 房屋区域
        # 居中显示

        self.label_region = tk.Label(self, text="房屋区域:")
        self.label_region.grid(row=1, column=0, sticky="ew")
        self.region_options = list(encoding_dict['房屋区域'].keys())  # 获取所有区域的选择
        self.region_var = tk.StringVar()
        self.region_dropdown = tk.OptionMenu(self, self.region_var, *self.region_options)
        self.region_dropdown.grid(row=1, column=1)

        # 房屋面积
        self.label_size = tk.Label(self, text="房屋面积:")
        self.label_size.grid(row=2, column=0, sticky="ew", padx=10)
        self.entry_size = tk.Entry(self)
        self.entry_size.grid(row=2, column=1)

        # 装修
        self.label_renovation = tk.Label(self, text="装修:")
        self.label_renovation.grid(row=3, column=0, sticky="ew", padx=10)
        self.renovation_options = list(encoding_dict['装修'].keys())  # 获取所有装修选项
        self.renovation_var = tk.StringVar()
        self.renovation_dropdown = tk.OptionMenu(self, self.renovation_var, *self.renovation_options)
        self.renovation_dropdown.grid(row=3, column=1)

        # 室输入框 (改为选择框)
        self.label_room = tk.Label(self, text="室:")
        self.label_room.grid(row=4, column=0, sticky="ew", padx=10)
        self.room_options = [i for i in range(1, 6)]  # 假设最多5个室
        self.room_var = tk.StringVar()
        self.room_dropdown = tk.OptionMenu(self, self.room_var, *self.room_options)
        self.room_dropdown.grid(row=4, column=1)

        # 厅输入框 (改为选择框)
        self.label_hall = tk.Label(self, text="厅:")
        self.label_hall.grid(row=5, column=0, sticky="ew", padx=10)
        self.hall_options = [i for i in range(1, 6)]  # 假设最多5个厅
        self.hall_var = tk.StringVar()
        self.hall_dropdown = tk.OptionMenu(self, self.hall_var, *self.hall_options)
        self.hall_dropdown.grid(row=5, column=1)

        # 楼层选择框 (改为选择框)
        self.label_floor = tk.Label(self, text="楼层:")
        self.label_floor.grid(row=6, column=0, sticky="ew", padx=10)
        self.floor_options = list(encoding_dict['楼层'].keys())  # 获取所有楼层选项
        self.floor_var = tk.StringVar()
        self.floor_dropdown = tk.OptionMenu(self, self.floor_var, *self.floor_options)
        self.floor_dropdown.grid(row=6, column=1)

        # 年份
        self.label_year = tk.Label(self, text="年份:")
        self.label_year.grid(row=7, column=0, sticky="ew", padx=10)
        self.entry_year = tk.Entry(self)
        self.entry_year.grid(row=7, column=1, sticky="ew")

        # 房屋类型
        self.label_type = tk.Label(self, text="房屋类型:")
        self.label_type.grid(row=8, column=0, sticky="e", padx=10)
        self.house_type_options = list(encoding_dict['房屋类型'].keys())  # 获取所有房屋类型
        self.house_type_var = tk.StringVar()
        self.house_type_dropdown = tk.OptionMenu(self, self.house_type_var, *self.house_type_options)
        self.house_type_dropdown.grid(row=8, column=1)

        # 县区
        self.label_county = tk.Label(self, text="县区:")
        self.label_county.grid(row=9, column=0, sticky="e", padx=10)
        self.county_options = list(encoding_dict['县区'].keys())  # 获取所有县区选项
        self.county_var = tk.StringVar()
        self.county_dropdown = tk.OptionMenu(self, self.county_var, *self.county_options)
        self.county_dropdown.grid(row=9, column=1)

        # 模型选择
        self.label_model = tk.Label(self, text="选择模型:")
        self.label_model.grid(row=10, column=0, sticky="e", padx=10)
        self.model_var = tk.StringVar()
        # 文件夹里面的模型
        self.model_options = ["LinearRegression", "RandomForest", "GradientBoosting"]
        self.model_dropdown = tk.OptionMenu(self, self.model_var, *self.model_options)
        self.model_var.set(self.selected_model)  # 默认选择RandomForest
        self.model_dropdown.grid(row=10, column=1)

        # 预测按钮
        self.predict_button = tk.Button(self, text="预测房价", command=self.predict_price)
        self.predict_button.grid(row=11, column=0, columnspan=2, pady=20)

        # 预测结果显示
        self.result_label = tk.Label(self, text="预测房价：", font=("Arial", 12))
        self.result_label.grid(row=12, column=0, columnspan=2, pady=10)

        # 显示相似的房源
        # 使用表格显示相似的房源
        self.similar_label = tk.Label(self, text="相似房源信息：", font=("Arial", 10))
        self.similar_label.grid(row=13, column=0, columnspan=2, pady=10)

    def predict_price(self):
        try:
            # 获取用户输入的房屋信息
            region = self.region_var.get()
            size = float(self.entry_size.get())
            renovation = self.renovation_var.get()
            house_type = self.house_type_var.get()
            floor = self.floor_var.get()
            year = int(self.entry_year.get())
            county = self.county_var.get()
            room = int(self.room_var.get())
            hall = int(self.hall_var.get())

            # 编码用户输入
            encoded_input = {
                '房屋区域': encoding_dict['房屋区域'].get(region, -1),
                '房屋面积': size,
                '装修': encoding_dict['装修'].get(renovation, -1),
                '楼层': encoding_dict['楼层'].get(floor, -1),
                '年份': year,
                '房屋类型': encoding_dict['房屋类型'].get(house_type, -1),
                '县区': encoding_dict['县区'].get(county, -1),
                '室': room,
                '厅': hall
            }

            # 检查编码值是否有效
            if -1 in encoded_input.values():
                raise ValueError("输入数据无效，请检查输入的字段")

            # 按照训练时的特征顺序创建输入数据
            input_data = pd.DataFrame([[
                encoded_input['房屋区域'],
                encoded_input['房屋面积'],
                encoded_input['装修'],
                encoded_input['楼层'],
                encoded_input['年份'],
                encoded_input['房屋类型'],
                encoded_input['县区'],
                encoded_input['室'],
                encoded_input['厅']
            ]], columns=columns)

            # 加载模型
            model_filename = f"{self.model_var.get().lower()}_model.pkl"
            with open(model_filename, 'rb') as f:
                model = pickle.load(f)


            # 加载模型并预测
            predicted_price = model.predict(input_data)[0]

            # 显示预测结果
            self.result_label.config(text=f"预测房价：{predicted_price:.2f}万元")

            # 推荐相似房源（通过计算距离）
            self.recommend_similar_houses(encoded_input)

        except ValueError as e:
            messagebox.showerror("输入无效", str(e))

    def recommend_similar_houses(self, encoded_input):
        # 读取数据
        data = pd.read_csv("data.csv")

        # 解码所有编码特征为原始字符串
        def decode_column(data, column):
            return data[column].map(lambda x: encoding_dict[column].get(x, x))

        # 解码所有需要显示的特征
        data['房屋区域'] = decode_column(data, '房屋区域')
        data['装修'] = decode_column(data, '装修')
        data['房屋类型'] = decode_column(data, '房屋类型')
        data['县区'] = decode_column(data, '县区')

        # 计算欧氏距离
        def euclidean_distance(row):
            distance = np.sqrt(
                (row['房屋区域'] != encoded_input['房屋区域']) ** 2 +
                (row['房屋面积'] - encoded_input['房屋面积']) ** 2 +
                (row['装修'] != encoded_input['装修']) ** 2 +
                (row['楼层'] - encoded_input['楼层']) ** 2 +
                (row['年份'] - encoded_input['年份']) ** 2 +
                (row['房屋类型'] != encoded_input['房屋类型']) ** 2 +
                (row['县区'] != encoded_input['县区']) ** 2 +
                (row['室'] - encoded_input['室']) ** 2 +
                (row['厅'] - encoded_input['厅']) ** 2
            )
            return distance

        # 计算所有房源与输入的房源之间的欧氏距离
        data['距离'] = data.apply(euclidean_distance, axis=1)

        # 获取距离最小的5个房源
        similar_houses = data.nsmallest(5, '距离')

        # 显示这些房源的简要信息
        similar_text = ""
        # 逆向映射字典，假设你已经保存了编码时的字典
        reverse_encoding_dict = {
            '房屋区域': {v: k for k, v in encoding_dict['房屋区域'].items()},
            '装修': {v: k for k, v in encoding_dict['装修'].items()},
            '房屋类型': {v: k for k, v in encoding_dict['房屋类型'].items()},
            '县区': {v: k for k, v in encoding_dict['县区'].items()},
            '楼层': {v: k for k, v in encoding_dict['楼层'].items()}
        }

        for i, house in similar_houses.iterrows():
            # 获取原始的房屋数据
            original_data = {
                '房屋区域': reverse_encoding_dict['房屋区域'].get(house['房屋区域'], house['房屋区域']),
                '房屋面积': house['房屋面积'],
                '装修': reverse_encoding_dict['装修'].get(house['装修'], house['装修']),
                '楼层': reverse_encoding_dict['楼层'].get(house['楼层'], house['楼层']),
                '年份': house['年份'],
                '房屋类型': reverse_encoding_dict['房屋类型'].get(house['房屋类型'], house['房屋类型']),
                '县区': reverse_encoding_dict['县区'].get(house['县区'], house['县区']),
                '室': house['室'],
                '厅': house['厅'],
                '价格': house['价格']
            }

            # 在这里显示原始的编码前信息
            similar_text += f"房屋区域: {original_data['房屋区域']} | 面积: {original_data['房屋面积']} | 装修: {original_data['装修']} | "
            similar_text += f"楼层: {original_data['楼层']} | 年份: {original_data['年份']} | 房屋类型: {original_data['房屋类型']} | "
            similar_text += f"县区: {original_data['县区']} | 室: {original_data['室']} | 厅: {original_data['厅']} | 价格: {original_data['价格']}万元\n"

        # 更新Label显示的文本
        self.similar_label.config(text=similar_text)

# 启动界面
if __name__ == "__main__":
    app = HousePricePredictor()
    app.mainloop()
