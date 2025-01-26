import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import pickle

# 读取数据
data = pd.read_csv("data.csv")

# 分离特征和目标变量
X = data[['房屋区域', '室', '厅', '房屋面积', '装修', '楼层', '年份', '房屋类型', '县区']]
y = data['价格']

# 复制 X 防止 SettingWithCopyWarning
X = X.copy()

# 数值特征标准化
scaler = StandardScaler()
X[['房屋面积', '年份', '室', '厅']] = scaler.fit_transform(X[['房屋面积', '年份', '室', '厅']])

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化模型
models = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "Linear Regression": LinearRegression()
}

# 用于存储评估结果
results = {}

# 遍历所有模型
for model_name, model in models.items():
    # 训练模型
    model.fit(X_train, y_train)

    # 预测结果
    y_pred = model.predict(X_test)

    # 模型评估
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 存储评估结果
    results[model_name] = {
        "MSE": mse,
        "MAE": mae,
        "R2 Score": r2
    }

    # 保存模型
    model_filename = f"{model_name.replace(' ', '').lower()}_model.pkl"
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"{model_name} 已保存为 {model_filename}")

# 打印模型评估结果
print("\n模型评估结果：")
for model_name, metrics in results.items():
    print(f"\n{model_name}:")
    for metric_name, value in metrics.items():
        print(f"{metric_name}: {value:.4f}")
