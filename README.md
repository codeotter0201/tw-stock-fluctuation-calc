# 台灣股票漲跌幅計算工具

這個 Python 工具專為計算台灣股票市場的漲跌幅設計。根據台灣證券交易所的規定，不同價格區間的股票有特定的漲跌點數限制。這個工具可以幫助您快速計算任何給定股價的漲跌幅範圍。

參考網址: https://www.twse.com.tw/zh/products/system/trading.html#:~:text=%E4%BE%9D%E7%87%9F%E6%A5%AD%E7%B4%B0%E5%89%87%E7%AC%AC62,%E7%95%B6%E6%97%A5%E6%BC%B2%E5%81%9C%E5%83%B9%E6%A0%BC%E6%87%89%E7%82%BA

## 功能

- 根據輸入的股價，計算其允許的最低和最高價格範圍
- 嚴格遵守台灣證券交易所的漲跌幅規則
- 驗證輸入價格是否符合特定區間的規則
- 處理各種邊界情況和無效輸入

## 使用方法

1. 導入必要的函數：

```python
from taiwan_stock_calculator import create_price_table, get_price_range, InvalidPriceError
```

2. 創建價格表（這包含了台灣股市的漲跌點數規則）：

```python
price_ranges = create_price_table()
```

3. 使用 `get_price_range` 函數計算股價的漲跌幅範圍：

```python
try:
    lower_limit, upper_limit = get_price_range(price, price_ranges)
    print(f"股價 {price} 的漲跌幅範圍: {lower_limit} - {upper_limit}")
except InvalidPriceError as e:
    print(f"錯誤: {e}")
```

## 台灣股市漲跌點數規則

| 股價範圍 | 漲跌點數 |
|---------|---------|
| 0.01元 ~ 5元 | 0.01 |
| 5元 ~ 10元 | 0.01 |
| 10元 ~ 50元 | 0.05 |
| 50元 ~ 100元 | 0.1 |
| 100元 ~ 150元 | 0.5 |
| 150元 ~ 500元 | 0.5 |
| 500元 ~ 1000元 | 1.0 |
| 1000元以上 | 5.0 |

## 注意事項

- 股價必須是正數，且不小於 0.01 元
- 股價不能超過 1,000,000 元（工具設定的上限，可根據需要調整）
- 每個價格區間都有特定的小數位數要求：
  - 0.01-10元：最多2位小數
  - 10-50元：必須是0.05的倍數
  - 50-100元：必須是0.1的倍數
  - 100-500元：必須是0.5的倍數
  - 500-1000元：必須是整數
  - 1000元以上：必須是5的倍數且為整數

## 錯誤處理

函數會在遇到無效輸入時拋出 `InvalidPriceError` 異常，包括：
- 非數字輸入
- 負數或零
- 不符合區間規則的股價
- 超出允許範圍的股價

## 示例

```python
price_ranges = create_price_table()

try:
    lower, upper = get_price_range(75.5, price_ranges)
    print(f"股價 75.5 元的漲跌幅範圍: {lower} - {upper}")
except InvalidPriceError as e:
    print(f"錯誤: {e}")

# 輸出: 股價 75.5 元的漲跌幅範圍: 75.4 - 75.6
```

## 應用場景

- 股票交易系統：快速計算買賣單是否在允許範圍內
- 風險管理：評估股票價格波動的合規性
- 回測系統：在歷史數據分析中確保價格變動符合規則
- 市場監控：檢測異常的價格波動

## 免責聲明

這個工具僅供參考和教育目的。在進行實際交易時，請務必遵循台灣證券交易所的官方規定和最新公告。