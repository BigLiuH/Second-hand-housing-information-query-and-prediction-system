import sqlite3
import pandas as pd



file_path="房源.csv"
infos=pd.read_csv(file_path,encoding="utf-8")

conn = sqlite3.connect('房源.db')
cursor = conn.cursor()
infos.to_sql('房源', conn, if_exists='replace', index=False)


# 关闭数据库连接
conn.close()