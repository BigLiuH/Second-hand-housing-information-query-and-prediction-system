import random
import pandas as pd
import tkinter as tk
from tkinter import ttk
import logging
import sys
sys.stdin

# 设置日志配置
logging.basicConfig(filename='system_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')


# 城市、位置和户型选项
# 使用这些作为城市名
cities = {
    '北京': ['朝阳', '海淀', '东城', '西城', '丰台'],
    '上海': ['浦东', '徐汇', '虹口', '黄浦', '长宁'],
    '广州': ['天河', '越秀', '荔湾', '白云', '番禺'],
    '深圳': ['南山', '福田', '宝安', '龙岗', '盐田'],
    '杭州': ['西湖', '上城', '下城', '滨江', '余杭'],
    '成都': ['青羊', '锦江', '金牛', '成华', '武侯'],
    '重庆': ['渝中', '沙坪坝', '南岸', '九龙坡', '江北'],
    '南京': ['玄武', '秦淮', '鼓楼', '雨花台', '浦口'],
    '武汉': ['江岸', '江汉', '硚口', '武昌', '青山'],
    '天津': ['和平', '南开', '红桥', '河东', '河西'],
    '西安': ['碑林', '雁塔', '新城', '未央', '长安'],
    '长沙': ['天心', '岳麓', '芙蓉', '开福', '雨花'],
    '沈阳': ['和平', '皇姑', '大东', '铁西', '苏家屯'],
    '青岛': ['市南', '市北', '黄岛', '崂山', '城阳'],
    '郑州': ['中原', '金水', '二七', '管城', '惠济'],
    '苏州': ['姑苏', '相城', '吴中', '工业园区', '虎丘'],
    '佛山': ['禅城', '南海', '顺德', '高明', '三水'],
    '东莞': ['莞城', '南城', '东城', '万江', '石碣'],
    '厦门': ['思明', '湖里', '集美', '海沧', '同安'],
    '合肥': ['瑶海', '蜀山', '包河', '庐阳', '肥西']
}

room_types = ['1B1B', '2B1B', '2B2B', '3B1B', '3B2B', '4B2B', '4B3B', '5B3B'] # 1B2B 一室两厅
prices = range(400000, 10000000, 50000)  # 价格范围40万到1000万

# 我通过上述三个变量的随机组合生成测试数据
# 随机数据生成函数
def generate_data(num_records=1500):# 参数是测试数据数量
    data = []
    for _ in range(num_records):
        city = random.choice(list(cities.keys()))# 随机获取城市名
        location = random.choice(cities[city])# 随机获取城市下的地区名
        room_type = random.choice(room_types)# 随机使用房型
        price = random.choice(prices)# 随机生成房价
        data.append([city, location, room_type, price])# 将数据加到列表里面

    df = pd.DataFrame(data, columns=['City', 'Location', 'Room_Type', 'Price'])
    df.to_csv('data.csv', index=False, encoding='utf-8')
    print("数据已生成并保存至'data.csv'")


# 生成测试数据
# generate_data()

# 主系统框架
class System:
    def __init__(self):
        # 加载CSV数据
        self.data = pd.read_csv('data.csv')
        logging.info("系统初始化完成，数据导入")
        self.root =tk.Tk()
        self.root.title("房价查询系统")
        self.root.geometry("1200x600")
        self.city=self.data['City'].unique().tolist()
        self.location=self.data['Location'].unique().tolist()
        self.room_type=self.data['Room_Type'].unique().tolist()

    def interface1(self):
        self.lable1 = tk.Label(self.root,text="房价查询系统",font=("微软雅黑",20))
        self.lable1.pack()

    def getcity(self):
        self.stringvar1 = tk.StringVar()
        self.stringvar1.set("请选择城市")

        # 创建城市选择下拉框
        self.citybox = ttk.Combobox(
            master=self.root,  # 父容器
            height=5,  # 高度,下拉显示的条目数量
            width=20,  # 宽度
            state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 15),  # 字体
            textvariable=self.stringvar1,  # 通过StringVar设置可改变的值
            values=self.city,  # 设置下拉框的选项
        )
        self.citybox.bind("<<ComboboxSelected>>", self.update_location)  # 绑定城市选择事件
        self.citybox.pack()  # 将下拉框添加到窗口中
        self.citybox.current(0)  # 默认选中第一个城市
        self.update_location()  # 默认更新 location 的选项
        self.update_room_type()
    def update_location(self, event=None):
        # 获取当前选择的城市
        selected_city = self.citybox.get()
        print("当前选择的城市是:", selected_city)

        # 根据选中的城市筛选出相应的区域
        temp = self.data[self.data['City'] == selected_city]['Location'].unique().tolist()

        # 更新 location 下拉框的选项
        if hasattr(self, 'locationbox'):
            self.locationbox.set('')  # 清空当前选择
            self.locationbox['values'] = temp  # 更新 location 下拉框的选项
        else:
            # 如果 locationbox 还未创建，则创建它
            self.stringvar2 = tk.StringVar()
            self.stringvar2.set("请选择城市区域")

            self.locationbox = ttk.Combobox(
                master=self.root,  # 父容器
                height=5,  # 高度,下拉显示的条目数量
                width=20,  # 宽度
                state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
                cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
                font=('', 15),  # 字体
                textvariable=self.stringvar2,  # 通过StringVar设置可改变的值
                values=temp,  # 设置下拉框的选项
            )
            self.locationbox.bind("<<ComboboxSelected>>", self.update_room_type)  # 绑定区域选择事件
            self.locationbox.pack()  # 将下拉框添加到窗口中
            self.update_room_type()  # 选择城市后更新房型

    def update_room_type(self, event=None):
        # 获取当前选择的城市和区域
        selected_city = self.citybox.get()
        selected_location = self.locationbox.get()

        print(f"选择的城市: {selected_city}")
        print(f"选择的区域: {selected_location}")

        # 根据选中的城市和区域筛选房间类型
        temp = self.data[self.data['City'] == selected_city]
        temp = temp[temp['Location'] == selected_location]['Room_Type'].unique().tolist()

        # 如果没有房型，给出提示
        if len(temp) == 0:
            print("没有找到匹配的房型，请检查城市或区域选择是否正确。")
            return

        # 清空并更新房间类型下拉框的选项
        if hasattr(self, 'roombox'):
            self.roombox.set('')  # 清空当前选择
            self.roombox['values'] = temp  # 更新房间类型下拉框的选项
        else:
            # 如果 roombox 还未创建，则创建它
            self.stringvar3 = tk.StringVar()
            self.stringvar3.set("请选择户型")

            self.roombox = ttk.Combobox(
                master=self.root,  # 父容器
                height=5,  # 高度,下拉显示的条目数量
                width=20,  # 宽度
                state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
                cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
                font=('', 15),  # 字体
                textvariable=self.stringvar3,  # 通过StringVar设置可改变的值
                values=temp,  # 设置下拉框的选项
            )
            self.roombox.bind("<<ComboboxSelected>>", self.getroom)
            self.roombox.pack()

    def getroom(self, event):
        print("当前选择的户型是:", self.roombox.get())
        return self.roombox.get()
    def search_properties(self, event=None):
        selected_city = self.citybox.get() if self.citybox.get() != "" else None
        selected_location = self.locationbox.get() if self.locationbox.get() != "" else None
        selected_room_type = self.roombox.get() if self.roombox.get() != "" else None

        # 筛选条件
        filtered_data = self.data
        if selected_city:
            filtered_data = filtered_data[filtered_data['City'] == selected_city]
        if selected_location:
            filtered_data = filtered_data[filtered_data['Location'] == selected_location]
        if selected_room_type:
            filtered_data = filtered_data[filtered_data['Room_Type'] == selected_room_type]

        # 在界面上显示查询结果
        self.display_results(filtered_data)

    def display_results(self, filtered_data):
        if hasattr(self, 'result_label'):
            self.result_label.destroy()

        # 使用滚动条框架
        result_frame = tk.Frame(self.root, bg='white', bd=5, relief="groove")
        result_frame.pack(pady=20, padx=50, fill="both", expand=True)

        if filtered_data.empty:
            self.result_label = tk.Label(result_frame, text="没有符合条件的房源", font=("微软雅黑", 16, "bold"), fg='red', bg='white')
            self.result_label.pack(pady=20)
        else:
            result_text = filtered_data.to_string(index=False)

            self.canvas = tk.Canvas(result_frame)
            self.scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas, bg='white')
            self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

            self.result_label = tk.Label(self.frame, text="查询结果：\n" + result_text, font=("微软雅黑", 12), fg="black", bg="white")
            self.result_label.pack(pady=10, padx=10)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scrollbar.grid(row=0, column=1, sticky="ns")

            result_frame.grid_rowconfigure(0, weight=1)
            result_frame.grid_columnconfigure(0, weight=1)


    def on_search_button_click(self):
        # 获取当前选择的城市、区域、房型
        selected_city = self.citybox.get() if self.citybox.get() != "" else None
        selected_location = self.locationbox.get() if self.locationbox.get() != "" else None
        selected_room_type = self.roombox.get() if self.roombox.get() != "" else None

        if selected_city == "":
            selected_city = None
        if selected_location == "":
            selected_location = None
        if selected_room_type == "":
            selected_room_type = None
        # 调用 search_properties 方法进行查询
        self.search_properties()

    def run(self):
        self.interface1()
        self.getcity()

        self.root.mainloop()

# 启动系统
if __name__ == "__main__":
    system = System()
    search_button = tk.Button(system.root, text="查询", font=("微软雅黑", 15), command=system.on_search_button_click)
    search_button.pack(pady=20)
    system.run()
