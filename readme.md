# High Volume Trade Monitoring

## 项目简介
本项目旨在通过与 Interactive Brokers (IB) 的 API 集成，实时监控股票的高成交量和价格波动情况，并在满足特定条件时触发警报。

## 功能
- **历史数据加载**：从 IB 获取股票的历史成交量数据，用于计算基准成交量。
- **实时数据订阅**：订阅股票的实时市场数据，包括价格和成交量。
- **超额交易检测**：基于实时数据，检测成交量是否超过基准成交量的阈值。
- **价格波动检测**：监控价格的涨跌幅是否超过设定的阈值。
- **报警机制**：在满足成交量和价格波动条件时触发警报。

## 依赖
- Python 3.8 或更高版本
- 以下 Python 库：
  - `asyncio`
  - `pandas`
  - `numpy`
  - `ib_insync`
  - `logging`

## 安装
1. 克隆项目到本地：
   ```bash
   git clone <repository-url>
   cd high_volume_trade