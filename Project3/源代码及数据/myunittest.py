import unittest
from fastapi.testclient import TestClient

from Project3.server import loaddata
from server import app,loaddata # 假设你的 FastAPI 应用保存在 'your_app_file.py' 中
import sqlite3


class TestFastAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 设置 SQLite 数据库，以便测试时不影响正式数据库
        cls.conn = sqlite3.connect(":memory:")  # 使用内存数据库进行测试
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS 房源 (
                link TEXT,
                address TEXT,
                style TEXT,
                area TEXT,
                towards TEXT,
                decoration TEXT,
                floor TEXT,
                years TEXT,
                building_type TEXT,
                price TEXT,
                city TEXT
            )""")
        cls.conn.commit()

        # 将数据库连接注入到 FastAPI 应用中
        app.state.db = cls.conn

    @classmethod
    def tearDownClass(cls):
        # 清理数据库连接
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        # 创建 TestClient 实例
        self.client = TestClient(app)

    def test_read_root(self):
        # 测试根路由
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "房源接口"})

    def test_get_houses(self):
        # 测试获取房屋信息的路由
        # 先插入一些数据
        # self.cursor.execute("""
        #     INSERT INTO 房源 (link, address, style, area, towards, decoration, floor, years, building_type, price, city)
        #     VALUES ('link1', 'address1', 'style1', '50', 'north', 'simple', '3', '5', 'apartment', '3000', '沈阳')
        # """)
        self.conn.commit()
        response = self.client.get("/houses")
        self.assertEqual(response.status_code, 200)
        houses = response.json().get("houses")
        self.assertGreater(len(houses), 0)  # 确保返回了房屋数据
        self.assertEqual(houses[0]["link"], "https://sy.lianjia.com/ershoufang/102107612704.html")  # 验证插入的数据是否正确返回

    def test_loaddata(self):
        # 测试 loaddata 函数的执行
        # 可以通过 mock 数据进行测试，检查 CSV 文件是否正确生成
        # 注意：此测试不涉及文件操作，假设其已被封装为某个功能函数
        data = loaddata()  # 假设 loaddata 在你的代码中定义且工作正常
        self.assertGreater(len(data), 0)  # 验证数据是否加载成功


if __name__ == "__main__":
    unittest.main()
