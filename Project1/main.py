import random
import pandas as pd
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
def generate_data(num_records=1000):# 参数是测试数据数量
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
generate_data()


# 主系统框架
class System:
    def __init__(self):
        # 加载CSV数据
        self.data = pd.read_csv('data.csv')
        logging.info("系统初始化完成，数据导入")

    def display_options(self):
        print("可选城市和位置：")
        for city, locations in cities.items():
            print(f" - {city}: {', '.join(locations)}")
        print("\n可选户型：")
        print(", ".join(room_types))
        print("\n")

    def search_properties(self, city=None, location=None, room_type=None):
        # 筛选条件
        filtered_data = self.data
        if city:
            filtered_data = filtered_data[filtered_data['City'] == city]
        if location:
            filtered_data = filtered_data[filtered_data['Location'] == location]
        if room_type:
            filtered_data = filtered_data[filtered_data['Room_Type'] == room_type]

        if filtered_data.empty:
            logging.info("没有符合条件的房源")
            print("没有符合条件的房源")
        else:
            logging.info("找到符合条件的房源")
            print("查询结果：")
            print(filtered_data)

    def run(self):
        print("欢迎使用二手房查询与房价预测系统")
        while True:
            print("\n1. 查询房源\n2. 退出")
            choice = input("请输入选项: ")
            if choice == '1':
                self.display_options()  # 显示可选项
                city = input("请输入城市: ")
                location = input("请输入区域: ")
                room_type = input("请输入户型(例: 2B1B): ")
                self.search_properties(city, location, room_type)
            elif choice == '2':
                logging.info("系统退出")
                print("退出系统")
                break
            else:
                logging.warning("无效选项")
                print("无效选项，请重试")


# 启动系统
if __name__ == "__main__":
    system = System()
    system.run()
