import asyncio
import pandas as pd
import numpy as np
from ib_insync import *
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

import logging

# 配置日志
logging.getLogger('ib_insync').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler("high_volume.log", when="MIDNIGHT")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# 连接到 IB
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # 调整端口为你的 TWS/IB Gateway 设置

# 读取股票列表
stocks_df = pd.read_csv('stocks.csv')  # 确保 CSV 文件路径正确
symbols = stocks_df['symbol'].tolist()[:100]  # 限制为 100 支股票
contracts = [Stock(symbol, 'SMART', 'USD') for symbol in symbols]

# 数据存储
data = {symbol: {
    'prices': [],  # 存储最近价格
    'volumes': [],  # 存储最近成交量
    'timestamps': [],  # 存储时间戳
    'base_volume': None,  # 历史平均成交量
    'last_alert': None  # 最后报警时间
} for symbol in symbols}

# 定义超额买卖和涨跌幅参数
VOLUME_THRESHOLD = 3.0  # 成交量超过均值的倍数
PRICE_CHANGE_THRESHOLD = 0.003  # 涨跌幅 0.3%
TIME_WINDOW = 3  # 3 秒窗口
ALERT_COOLDOWN = 60  # 报警冷却时间（秒）


# 获取历史数据以计算基准成交量
async def fetch_historical_volume(contract, symbol):
    try:
        bars = await ib.reqHistoricalDataAsync(
            contract,
            endDateTime='',
            durationStr='1 D',  # 1 天数据
            barSizeSetting='1 min',  # 1 分钟K线
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )
        if bars:
            volumes = [bar.volume for bar in bars]
            data[symbol]['base_volume'] = np.mean(volumes) if volumes else 1
            logger.info(f"{symbol} 基准成交量: {data[symbol]['base_volume']:.2f}")
        else:
            data[symbol]['base_volume'] = 1  # 默认值防止除零
    except Exception as e:
        logger.error(f"获取 {symbol} 历史数据失败: {e}")
        data[symbol]['base_volume'] = 1


# 实时数据处理
def on_tick(contract, tick):
    symbol = contract.symbol
    timestamp = datetime.now()
    price = tick.last if tick.last else tick.close
    volume = tick.volume if tick.volume else 0

    if price and volume:
        data[symbol]['prices'].append(price)
        data[symbol]['volumes'].append(volume)
        data[symbol]['timestamps'].append(timestamp)

        # 清理超过 3 秒的数据
        cutoff = timestamp - timedelta(seconds=TIME_WINDOW)
        data[symbol]['prices'] = [p for t, p in zip(data[symbol]['timestamps'], data[symbol]['prices']) if t > cutoff]
        data[symbol]['volumes'] = [v for t, v in zip(data[symbol]['timestamps'], data[symbol]['volumes']) if t > cutoff]
        data[symbol]['timestamps'] = [t for t in data[symbol]['timestamps'] if t > cutoff]

        # 检查超额买卖和涨跌幅
        check_alert(symbol)


# 检查是否需要报警
def check_alert(symbol):
    try:
        now = datetime.now()
        last_alert = data[symbol]['last_alert']
        if last_alert and (now - last_alert).total_seconds() < ALERT_COOLDOWN:
            return  # 冷却期内不报警

        volumes = data[symbol]['volumes']
        prices = data[symbol]['prices']
        base_volume = data[symbol]['base_volume']

        if len(volumes) < 2 or len(prices) < 2 or not base_volume:
            return  # 数据不足

        # 计算 3 秒内总成交量
        total_volume = sum(volumes)
        avg_volume_per_sec = total_volume / TIME_WINDOW

        # 检查超额买卖
        is_over_volume = avg_volume_per_sec > base_volume * VOLUME_THRESHOLD

        # 计算涨跌幅
        price_change = (prices[-1] - prices[0]) / prices[0] if prices[0] else 0
        is_price_moving = abs(price_change) > PRICE_CHANGE_THRESHOLD

        # 触发报警
        if is_over_volume and is_price_moving:
            direction = "上涨" if price_change > 0 else "下跌"
            logger.warning(
                f"警报: {symbol} 检测到超额交易! "
                f"成交量: {total_volume:.2f} (基准: {base_volume:.2f}), "
                f"涨跌幅: {price_change * 100:.2f}%, 方向: {direction}"
            )
            data[symbol]['last_alert'] = now

    except Exception as e:
        logger.error(f"处理 {symbol} 数据时出错: {e}")


# 主程序
async def main():
    # 预加载历史成交量
    for contract, symbol in zip(contracts, symbols):
        await fetch_historical_volume(contract, symbol)
        await asyncio.sleep(0.1)  # 避免请求过快

    # 订阅实时数据
    for contract in contracts:
        ib.reqMktData(contract, '', False, False)
        logger.info(f"订阅 {contract.symbol} 实时数据")

    with await ib.connectAsync():
        async for event in ib.pendingTickersEvent:
            for ticker in event:
                on_tick(ticker.contract, ticker)


# 运行程序
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序终止")
    finally:
        ib.disconnect()
