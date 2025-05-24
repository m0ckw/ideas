import pandas as pd
import os
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Publicly Traded Partnerships (PTP) 列表，这些股票将在回测中被排除
PTP = ['AAAA', 'AB', 'ABENU', 'AC', 'ACP', 'AFREZ', 'AGO', 'AGQ', 'AHGP', 'AHOTF', 'AIA', 'AIJ', 'AIK', 'AIRL', 'ALDW', 'ALT', 'AM', 'AMJ', 'AMLP', 'AMZA', 'ANDX', 'APL', 'APLP', 'APLVF', 'APO', 'APU', 'ARCX', 'ARLP', 'ARNPQ', 'ARPJQ',
       'ARPPQ', 'ATAX', 'ATLS', 'ATN', 'AZLCZ', 'AZURQ', 'BACR', 'BAR',
       'BARS', 'BBEPQ', 'BBPPQ', 'BBU', 'BDRY', 'BEP', 'BGH', 'BIP', 'BITW', 'BKEP', 'BKEPP', 'BNO', 'BNP', 'BNPC', 'BOIL', 'BPL', 'BPMP', 'BPY', 'BPYPM', 'BPYPN', 'BPYPO', 'BPYPP', 'BRENF', 'BRIPF', 'BSM', 'BTOU', 'BVERS', 'BWET', 'BWP',
       'CANE', 'CAPL', 'CCAP', 'CCLP', 'CCR', 'CEQP', 'CEQPPR',
       'CFD', 'CHC', 'CHKR', 'CIFC', 'CLMT', 'CMD', 'CMDT', 'CMLP', 'CMOU', 'CNPP', 'CNXM', 'CORN', 'CPER', 'CPLP', 'CPNO', 'CPPL', 'CQP', 'CRDE', 'CROC', 'CRPPE', 'CRUD', 'CTF', 'CVRR', 'CWPS', 'CWSRF', 'DBA', 'DBB', 'DBC', 'DBE', 'DBO',
       'DBP', 'DBS', 'DBV', 'DCP', 'DCPPRB', 'DCPPRC', 'DCR',
       'DCRU', 'DEFI', 'DEP', 'DFG', 'DGL', 'DIVVZ', 'DKL', 'DLNG', 'DMLP', 'DMM', 'DNO', 'DOY', 'ECSPQ', 'ECTM', 'ECTPQ', 'EEP', 'EFSH', 'EMESQ', 'ENBL', 'ENFR', 'ENGY', 'ENLK', 'ENP', 'EOTPQ', 'EPB', 'EPD', 'EPDU', 'EPE', 'EQGP', 'EQM',
       'EROC', 'ESBA', 'ET', 'ETP', 'ETPRC', 'ETPRD', 'ETPRE',
       'EUO', 'EVEPQ', 'EXLP', 'FELPQ', 'FGPR', 'FGPRB', 'FGPRQ', 'FISK', 'FOL', 'FRT', 'FSA', 'FSE', 'FSG', 'FSU', 'FTAI', 'FTAIN', 'FTAIO', 'FTAIP', 'FUN', 'FUTS', 'GBLI', 'GDAY', 'GDVTZ', 'GEL', 'GELPP', 'GFGY', 'GFWQZ', 'GGELU',
       'GGENU', 'GHI', 'GLL', 'GLOP', 'GLP', 'GLPPRA', 'GLPPRB', 'GPP',
       'GRP', 'GRP/U', 'GRPU', 'GS', 'GSG', 'GSJK', 'GTM', 'GWYGU', 'GYRO', 'HCRSQ', 'HEOL', 'HEP', 'HESM', 'HLND', 'HPG', 'HPGP', 'HRBGF', 'HRY', 'HTLLQ', 'IDIV', 'IEP', 'IEPRR', 'IGLPA', 'JPEP', 'KBSUF', 'KEPPF', 'KFN', 'KKR', 'KMP',
       'KOLD', 'KPEQF', 'KPP', 'KSL', 'KSP', 'LAACZ', 'LAZ', 'LINEQ',
       'LIW', 'LMRK', 'LMRKN', 'LMRKO', 'LMRKP', 'LNKE', 'LRE', 'MCEP', 'MDBH', 'MDWZZ', 'MEMPQ', 'MEP', 'MGG', 'MIZUHO', 'MLPA', 'MLPX', 'MMLP', 'MMP', 'MNR', 'MNULF', 'MPLX', 'MPLXP', 'MWE', 'MYTH', 'NAGS', 'NBLX', 'NEN', 'NEP', 'NGL',
       'NGLPRB', 'NGLPRC', 'NGLS', 'NGOOB', 'NGOOL', 'NGOWL', 'NHL',
       'NKA', 'NLP', 'NNUTU', 'NRGP', 'NRP', 'NS', 'NSLPQ', 'NSP', 'NSPRA', 'NSPRB', 'NSPRC', 'NTI', 'NUSPQ', 'OAK', 'OCIP', 'ODBU', 'OGCP', 'OILT', 'OKCMZ', 'OKS', 'OMP', 'OSP', 'OXF', 'OXMU', 'OZ', 'PAA', 'PAAPU', 'PAGP', 'PBFX', 'PDH',
       'PFDM', 'PLP', 'PNG', 'POPE', 'PPX', 'PR', 'PRA', 'PRB',
       'PRC', 'PRCL', 'PRD', 'PRE', 'PRI', 'PRT', 'PSE', 'PSXP', 'PTXP', 'PVR', 'QEPM', 'QRE', 'REGX', 'RGL', 'RGP', 'RISE', 'RMP', 'RNF', 'RRMS', 'RSE', 'RSTRF', 'RTW', 'RTWFF', 'SCO', 'SDRMU', 'SDTTU', 'SEP', 'SGH', 'SHLX', 'SIRE',
       'SMLP', 'SNMP', 'SOYB', 'SPH', 'SPKX', 'SPKY', 'SPLP', 'SRLP',
       'SUN', 'SVIX', 'SVXY', 'SWIOU', 'SXCP', 'SXEEQ', 'TAGS', 'TCGP', 'TCP', 'TEP', 'TESLU', 'TLP', 'TNH', 'TONS', 'TPP', 'TRIC', 'TRLC', 'TRLI', 'TXO', 'U', 'UAN', 'UCASU', 'UCD', 'UCLP', 'UCO', 'UCR', 'UDN', 'UGA', 'UGL', 'UHN', 'ULE',
       'UMI', 'UMM', 'UNG', 'UNHRF', 'UNL', 'UOY', 'USAC', 'USAG',
       'USCI', 'USDP', 'USL', 'USMI', 'USO', 'USOD', 'USOU', 'USSPQ', 'UUP', 'UVIX', 'UVXY', 'VEH', 'VIXM', 'VIXY', 'VLI', 'VLP', 'VNGBQ', 'VNRAQ', 'VNRCQ', 'VNRSQ', 'VPRB', 'VTDRF', 'WEAT', 'WEIX', 'WES', 'WLKP', 'WMLPQ', 'WMZ', 'WNRL',
       'WPG', 'WPG.', 'WPT', 'WPZ', 'XXFPL', 'XXMUT', 'YCL', 'YCS',
       'ZSL', 'ZZCDH']


def backtest(data_folder, file_pattern, start_date, end_date, min_price, number, monthly_return_threshold, plot=True):
    # ========== 加载所有股票数据 ==========
    all_files = glob(os.path.join(data_folder, file_pattern))

    stock_data = {}
    for file_path in all_files:
        ticker = os.path.basename(file_path).split('.')[0]
        df = pd.read_csv(file_path, parse_dates=['date'])
        df['ticker'] = ticker
        stock_data[ticker] = df

    combined_df = pd.concat(stock_data.values())
    combined_df.sort_values(['ticker', 'date'], inplace=True)

    # 过滤交易时间范围
    combined_df = combined_df[combined_df['date'] >= pd.to_datetime(start_date)]
    combined_df = combined_df[combined_df['date'] <= pd.to_datetime(end_date)]

    # ========== 提取每月月初/月末价格 ==========
    combined_df['year_month'] = combined_df['date'].dt.to_period('M')
    monthly_groups = combined_df.groupby(['ticker', 'year_month'])

    monthly_prices = monthly_groups.agg(
        month_start_date=('date', 'first'),
        open_price=('open', 'first'),
        month_end_date=('date', 'last'),
        close_price=('close', 'last'),
        high=('high', 'max'),
        low=('low', 'min'),
        volume=('volume', 'sum')
    ).reset_index()

    # ========== 回测主逻辑 ==========
    returns = []
    excluded_tickers = set()
    all_months = sorted(monthly_prices['year_month'].unique())

    print("\n====== 每月最大盈利与最大亏损股票 ======\n")
    for ym in all_months:
        month_df = monthly_prices[monthly_prices['year_month'] == ym].copy()

        # 检查上个月是否有数据
        prev_month = ym - 1
        if prev_month not in all_months:
            print(f"📅 {ym} 月: 上个月没有数据，跳过交易")
            continue

        excluded_tickers = set()

        # 计算上个月的涨幅
        prev_month_df = monthly_prices[monthly_prices['year_month'] == prev_month].copy()
        prev_month_df.loc[:, 'monthly_return'] = (prev_month_df['close_price'] / prev_month_df['open_price']) - 1
        excluded_tickers.update(prev_month_df[prev_month_df['monthly_return'] > monthly_return_threshold]['ticker'])
        excluded_tickers.update(prev_month_df[prev_month_df['monthly_return'] < -0.5]['ticker'])
        excluded_tickers.update(prev_month_df[prev_month_df['volume'] > 700000000]['ticker'])


        # 仅保留股价 >= min_price 且不在剔除名单中的股票
        filtered = month_df[
            (month_df['open_price'] >= min_price) &
            (~month_df['ticker'].isin(excluded_tickers)) &
            (~month_df['ticker'].isin(PTP))
            ].copy()

        if filtered.empty:
            continue

        # 选择价格最低的 number 支股票
        selected = filtered.nsmallest(number, 'open_price')
        if len(selected) < number:
            print(f"📅 {ym} 月: 没有符合条件的股票，跳过交易")
            continue
        selected['return'] = selected['close_price'] / selected['open_price'] - 1
        selected.sort_values('open_price', inplace=True)

        # 最大盈利与最大亏损
        best_stock = selected.loc[selected['return'].idxmax()]
        worst_stock = selected.loc[selected['return'].idxmin()]

        print(f"📅 {ym} 月: {selected['ticker'].tolist()}")
        month_return = selected['return'].mean()
        # 打印所有选中股票的收益率
        for _, row in selected.iterrows():
            print(f"  {row['ticker']}: 买入 {row['open_price']:.2f} → 卖出 {row['close_price']:.2f} | 收益率 {row['return']:.2%}")
        print("  平均收益率: {:.2%}".format(month_return))
        # print(f"✅ 最大盈利: {best_stock['ticker']} | 买入 {best_stock['open_price']:.2f} → 卖出 {best_stock['close_price']:.2f} | 收益率 {best_stock['return']:.2%}")
        # print(f"❌ 最大亏损: {worst_stock['ticker']} | 买入 {worst_stock['open_price']:.2f} → 卖出 {worst_stock['close_price']:.2f} | 收益率 {worst_stock['return']:.2%}")
        print('-' * 60)

        # 本月平均收益

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

    # ========== 绘制曲线图 ==========
    if plot:
        rcParams['axes.unicode_minus'] = False

        plt.figure(figsize=(10, 6))
        plt.plot(returns_df['month'], returns_df['mean_return'], label='Monthly average income', marker='o')
        plt.plot(returns_df['month'], returns_df['cumulative_return'], label='cumulative gain', marker='s')
        plt.xlabel('Month')
        plt.ylabel('Yield rate')
        plt.title('Monthly average income and cumulative income curve')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()


# 示例调用
backtest(
    data_folder='./stocks/',
    file_pattern='*.csv',
    start_date='2020-01-01',
    end_date='2023-12-31',
    min_price=1,
    number=10,
    monthly_return_threshold=0.6,
    plot=False
)
