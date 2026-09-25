# Import required libraries
# 导入需要的库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set plot style
# 设置绘图样式
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Generate simulated stock price data
# 生成模拟股票价格数据
np.random.seed(42)
days = 365
base_price = 100
# Simulate daily return
# 模拟每日收益率
daily_return = np.random.normal(0.0005, 0.02, days)
price_series = base_price * np.cumprod(1 + daily_return)

# Build dataframe
# 构建数据表
df = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=days, freq='D'),
    'price': price_series
})

# Calculate moving average
# 计算均线：短期20日均线，长期60日均线
df['ma_short'] = df['price'].rolling(window=20).mean()
df['ma_long'] = df['price'].rolling(window=60).mean()

# Generate trading signal
# 生成交易信号：1=买入持仓，0=空仓
df['signal'] = 0
# 金叉：短期均线上穿长期均线，买入
df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 1

# Calculate daily strategy return
# 计算策略每日收益
df['daily_return'] = df['price'].pct_change()
df['strategy_return'] = df['signal'].shift(1) * df['daily_return']

# Cumulative return
# 累计收益
df['cumulative_buyhold'] = (1 + df['daily_return']).cumprod()
df['cumulative_strategy'] = (1 + df['strategy_return']).cumprod()

# Calculate key metrics
# 计算关键指标：总收益、最大回撤
def max_drawdown(series):
    peak = series.cummax()
    drawdown = (series - peak) / peak
    return drawdown.min()

total_strategy_return = df['cumulative_strategy'].iloc[-1] - 1
total_bh_return = df['cumulative_buyhold'].iloc[-1] - 1
strategy_max_dd = max_drawdown(df['cumulative_strategy'])
bh_max_dd = max_drawdown(df['cumulative_buyhold'])

print("==== Strategy Performance ====")
print(f"Strategy Total Return: {total_strategy_return:.2%}")
print(f"Buy & Hold Total Return: {total_bh_return:.2%}")
print(f"Strategy Max Drawdown: {strategy_max_dd:.2%}")
print(f"Buy & Hold Max Drawdown: {bh_max_dd:.2%}")

# Plot result
# 绘制净值对比图
plt.figure(figsize=(12,6))
plt.plot(df['date'], df['cumulative_strategy'], label='Moving Average Strategy')
plt.plot(df['date'], df['cumulative_buyhold'], label='Buy and Hold')
plt.title('Portfolio Net Value Comparison')
plt.xlabel('Date')
plt.ylabel('Net Value')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('portfolio_curve.png', dpi=300, bbox_inches='tight')
plt.show()