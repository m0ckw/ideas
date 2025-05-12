from futu import *
import csv
# 初始化行情上下文
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 设置股价筛选条件
price_filter = SimpleFilter()
price_filter.filter_min = 2
price_filter.filter_max = 15
price_filter.stock_field = StockField.CUR_PRICE
price_filter.is_no_filter = False

# 设置市值筛选条件（单位：人民币）
market_val_filter = SimpleFilter()
market_val_filter.filter_min = 1e9  # 10亿
market_val_filter.filter_max = 2e10  # 200亿
market_val_filter.stock_field = StockField.MARKET_VAL
market_val_filter.is_no_filter = False

# # 设置成交量筛选条件（单位：股）
volume_filter = AccumulateFilter()
volume_filter.filter_min = 30000000  # 1000万股
volume_filter.stock_field = StockField.TURNOVER
volume_filter.is_no_filter = False

net_profit_filter = FinancialFilter()
net_profit_filter.filter_min = 5e7  # 10亿
net_profit_filter.stock_field = StockField.NET_PROFIT
net_profit_filter.is_no_filter = False
#
# 组合筛选条件
filter_list = [price_filter, market_val_filter, volume_filter, net_profit_filter]

# 执行筛选

stocks = []

start = 0
while True:
    ret, data = quote_ctx.get_stock_filter(market=Market.SH, filter_list=filter_list, begin=start, num=200)
    if ret == RET_OK:
        stocks.extend(data[2])
        print(data)
        if len(data[2]) != 200:
            print('筛选完成：', data)
            break
        start += 200
    else:
        print('筛选失败：', data)
        time.sleep(1)

# 将筛选结果保存到 CSV 文件
if stocks:
    csv_file = "filtered_stocks.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock Code", "Stock Name", "Current Price", "Market Value", "Turnover", "Net Profit"])  # 表头
        for stock in stocks:
            writer.writerow([
                stock.stock_code,
                stock.stock_name,
                stock.cur_price,
                stock.market_val,
            ])
    print(f"✅ 筛选结果已保存到 {csv_file}")
else:
    print("❌ 无筛选结果可保存。")

# 关闭行情上下文
quote_ctx.close()
