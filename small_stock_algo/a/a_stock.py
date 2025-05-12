import pandas as pd
import os
from datetime import datetime
from glob import glob

# ========== 配置 ==========
data_folder = './stocks/'  # CSV 文件夹路径
file_pattern = '*_5years_daily.csv'

# ========== 加载所有股票数据 ==========
all_files = glob(os.path.join(data_folder, file_pattern))

stock_data = {}
for file_path in all_files:
    ticker = os.path.basename(file_path).split('_')[0]
    df = pd.read_csv(file_path, parse_dates=['trade_date'])
    df['ticker'] = ticker
    stock_data[ticker] = df

combined_df = pd.concat(stock_data.values())
combined_df.sort_values(['ticker', 'trade_date'], inplace=True)

# ========== 提取每月月初/月末价格 ==========
combined_df['year_month'] = combined_df['trade_date'].dt.to_period('M')
monthly_groups = combined_df.groupby(['ticker', 'year_month'])

monthly_prices = monthly_groups.agg(
    month_start_date=('trade_date', 'first'),
    open_price=('open', 'first'),
    month_end_date=('trade_date', 'last'),
    close_price=('close', 'last')
).reset_index()

# ========== 回测主逻辑 ==========
returns = []
excluded_tickers = set()
all_months = sorted(monthly_prices['year_month'].unique())  # 确保顺序一致

print("\n====== 每月最大盈利与最大亏损股票 ======\n")
for ym in all_months:
    month_df = monthly_prices[monthly_prices['year_month'] == ym].copy()

    # 仅保留股价 >= 3 且不在剔除名单中的股票
    filtered = month_df[
        (month_df['open_price'] >= 1.5) & (~month_df['ticker'].isin(excluded_tickers))
        ].copy()

    if filtered.empty:
        continue

    # 检查上个月是否有数据
    prev_month = ym - 1
    if prev_month not in all_months:
        print(f"📅 {ym} 月: 上个月没有数据，跳过交易")
        continue

    excluded_tickers = set()

    # 计算上个月的涨幅
    prev_month_df = monthly_prices[monthly_prices['year_month'] == prev_month].copy()  # 添加 .copy()
    prev_month_df.loc[:, 'monthly_return'] = (prev_month_df['close_price'] / prev_month_df['open_price']) - 1
    excluded_tickers.update(prev_month_df[prev_month_df['monthly_return'] > 0.2]['ticker'])

    # 选择价格最低的 50 支股票
    selected = filtered.nsmallest(20, 'open_price')
    selected['return'] = selected['close_price'] / selected['open_price'] - 1

    # 最大盈利与最大亏损
    best_stock = selected.loc[selected['return'].idxmax()]
    worst_stock = selected.loc[selected['return'].idxmin()]

    print(f"📅 {ym} 月:")
    print(f"✅ 最大盈利: {best_stock['ticker']} | 买入 {best_stock['open_price']:.2f} → 卖出 {best_stock['close_price']:.2f} | 收益率 {best_stock['return']:.2%}")
    print(f"❌ 最大亏损: {worst_stock['ticker']} | 买入 {worst_stock['open_price']:.2f} → 卖出 {worst_stock['close_price']:.2f} | 收益率 {worst_stock['return']:.2%}")
    print('-' * 60)

    # 本月平均收益
    month_return = selected['return'].mean()

    # 存储结果
    returns.append({
        'month': str(ym),
        'mean_return': month_return,
        'best_ticker': best_stock['ticker'],
        'best_return': best_stock['return'],
        'worst_ticker': worst_stock['ticker'],
        'worst_return': worst_stock['return'],
        'excluded_next_month': list(excluded_tickers),
        'selected_tickers': selected['ticker'].tolist()
    })

# ========== 总结输出 ==========
returns_df = pd.DataFrame(returns)
returns_df['cumulative_return'] = (1 + returns_df['mean_return']).cumprod()

print("\n====== 每月平均收益与累计收益 ======\n")
print(returns_df[['month', 'mean_return', 'cumulative_return']])

final_return = returns_df['cumulative_return'].iloc[-1] - 1
print(f"\n📈 最终累计收益率: {final_return:.2%}")
