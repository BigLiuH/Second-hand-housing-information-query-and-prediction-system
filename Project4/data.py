import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import json


# 创建楼层类型列并进行分类编码
def encode_floor_type(floor_str):
    if '低楼层' in floor_str:
        return 0  # 低楼层
    elif '高楼层' in floor_str:
        return 2  # 高楼层
    else:
        return 1  # 中楼层，假设其他为中楼层

origin_data=pd.read_csv("沈阳.csv")

data=origin_data.copy()
# 数据清洗
# 户型分离为室和厅
data[['室', '厅']] = data['户型'].str.extract(r'(\d+)室(\d+)厅')

# 处理装修里面的其他数据
# 替换"装修"列中的“其他”为“简装”
data['装修'] = data['装修'].replace('其他', '简装')

# 楼层数据清洗
data = data[~data['楼层'].str.match(r'^\d+层$', na=False)]
# 应用函数编码楼层类型
data['楼层'] = data['楼层'].apply(encode_floor_type)
# 年份的处理
# 删除"年份"列中包含"暂无数据"的行
data = data[data['年份'] != '暂无数据']

# 删除"房屋类型"列中包含"暂无数据"的行
data = data[data['房屋类型'] != '暂无数据']

# 创建LabelEncoder对象
label_encoder = LabelEncoder()
# 使用fit_transform对“小区名称”列进行标签编码
class_feature=['房屋区域','装修','房屋类型','县区']
encoding_dict={}
for column in class_feature:
    # 对每列进行编码
    encoded_values = label_encoder.fit_transform(data[column])

    # 保存编码对照表
    encoding_dict[column] = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))

    # 更新数据
    data[column] = encoded_values

# data['小区名称'] = label_encoder.fit_transform(data['小区名称'])# 可能删除
# data['房屋区域'] = label_encoder.fit_transform(data['房屋区域'])
# data['朝向'] = label_encoder.fit_transform(data['朝向'])# 可能删除
# data['装修'] = label_encoder.fit_transform(data['装修'])
# data['房屋类型'] = label_encoder.fit_transform(data['房屋类型'])
# data['县区'] = label_encoder.fit_transform(data['县区'])

# 数值特征处理
data_features=['价格','房屋面积','年份','室','厅']
for column in data_features:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# data['价格'] = pd.to_numeric(data['价格'], errors='coerce')
# data['房屋面积']= pd.to_numeric(data['房屋面积'], errors='coerce')
# data['年份']= pd.to_numeric(data['年份'], errors='coerce')
# data['厅']= pd.to_numeric(data['厅'], errors='coerce')
# data['室']= pd.to_numeric(data['室'], errors='coerce')

# 删除数据
data = data.drop('户型', axis=1)
data = data.drop('朝向', axis=1)
data = data.drop('小区名称', axis=1)
print(encoding_dict)
encoding_dict['楼层']={'低楼层':0,'中楼层':1,'高楼层':2}
with open('encoding_mappings.json', 'w', encoding='utf-8') as f:
    json.dump(encoding_dict, f, ensure_ascii=False, indent=4)
# 将结果保存为新的CSV文件
data.to_csv('data.csv',index=False)
