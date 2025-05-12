import os
import time
import pandas as pd
import tushare as ts
from datetime import datetime, timedelta

# 初始化 tushare
ts.set_token('69e069909397db3849328462417ec6813c31b9af8bcecdfb9dbcb7cf')  # 替换为你的 Tushare API Token
pro = ts.pro_api()

# 读取股票代码
input_file = 'a_stocks.csv'
output_folder = './stocks/'
df = pd.read_csv(input_file)
stock_codes = df['Stock Code'].tolist()

# 获取最近 5 年的天级价格数据
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=5 * 365)).strftime('%Y%m%d')

for stock_code in stock_codes:
    stock_code = stock_code.split('.')[::-1]
    stock_code = '.'.join(stock_code)
    output_file = f"{output_folder}{stock_code}_5years_daily.csv"
    if os.path.exists(output_file):
        continue
    print(f"正在获取 {stock_code} 的数据...")
    try:
        data = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        if not data.empty:
            data.to_csv(output_file, index=False, encoding='utf-8')
            print(f"✅ {stock_code} 的数据已保存到 {output_file}")
        else:
            print(f"❌ {stock_code} 没有获取到数据")
    except Exception as e:
        print(f"❌ 获取 {stock_code} 的数据失败: {e}")
    time.sleep(0.1)