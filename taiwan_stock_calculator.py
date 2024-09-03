"""
這個 Python 工具專為計算台灣股票市場的漲跌幅設計。根據台灣證券交易所的規定，
不同價格區間的股票有特定的漲跌點數限制。這個工具可以幫助您快速計算任何給定股價的漲跌幅範圍。

參考網址: https://www.twse.com.tw/zh/products/system/trading.html#:~:text=%E4%BE%9D%E7%87%9F%E6%A5%AD%E7%B4%B0%E5%89%87%E7%AC%AC62,%E7%95%B6%E6%97%A5%E6%BC%B2%E5%81%9C%E5%83%B9%E6%A0%BC%E6%87%89%E7%82%BA
"""

from typing import List, Tuple
import bisect


class InvalidPriceError(Exception):
    pass


def create_price_table() -> List[Tuple[float, float, float]]:
    """
    創建並返回台灣股票市場的價格區間表。

    每個元組包含三個元素：
    1. 區間起始價格
    2. 區間結束價格（不包含）
    3. 該區間的漲跌幅度

    返回:
        List[Tuple[float, float, float]]: 價格區間表
    """
    ranges = [
        (0.01, 10, 0.01),
        (10, 50, 0.05),
        (50, 100, 0.1),
        (100, 150, 0.5),
        (150, 500, 0.5),
        (500, 1000, 1.0),
        (1000, float("inf"), 5.0),
    ]
    return ranges


def get_price_range(
    price: float, ranges: List[Tuple[float, float, float]]
) -> Tuple[float, float]:
    """
    計算給定股價的漲跌幅範圍。

    參數:
        price (float): 要計算漲跌幅的股價
        ranges (List[Tuple[float, float, float]]): 價格區間表

    返回:
        Tuple[float, float]: 包含下限價格和上限價格的元組

    異常:
        InvalidPriceError: 當輸入的價格無效或不符合規則時拋出
    """
    try:
        price = float(price)
    except ValueError:
        raise InvalidPriceError(
            f"Invalid price input: {price}. Price must be a number."
        )

    if price <= 0:
        raise InvalidPriceError(f"Price {price} is not positive.")

    if price < 0.01:
        raise InvalidPriceError(
            f"Price {price} is below the minimum allowed price of 0.01."
        )

    if price > 1000000:
        raise InvalidPriceError(
            f"Price {price} exceeds the maximum allowed price of 1,000,000."
        )

    # 使用二分搜索找到正確的價格區間
    index = bisect.bisect_right([r[0] for r in ranges], price) - 1
    start, end, fluctuation = ranges[index]

    # 檢查價格是否符合當前區間的規則
    if start <= price < 10 and not (price * 100).is_integer():
        raise InvalidPriceError(
            f"Price {price} in range 0.01-5 must have at most 2 decimal places."
        )
    elif 10 <= price < 50 and not (price * 20).is_integer():
        raise InvalidPriceError(
            f"Price {price} in range 10-50 must be a multiple of 0.05."
        )
    elif 50 <= price < 100 and not (price * 10).is_integer():
        raise InvalidPriceError(
            f"Price {price} in range 50-100 must be a multiple of 0.1."
        )
    elif 100 <= price < 500 and not (price * 2).is_integer():
        raise InvalidPriceError(
            f"Price {price} in range 100-500 must be a multiple of 0.5."
        )
    elif 500 <= price < 1000 and not price.is_integer():
        raise InvalidPriceError(f"Price {price} in range 500-1000 must be an integer.")
    elif price >= 1000 and not (price % 5 == 0 and price.is_integer()):
        raise InvalidPriceError(
            f"Price {price} above 1000 must be an integer multiple of 5."
        )

    # 特殊處理區間邊界
    if price == start and index > 0:
        down_fluctuation = ranges[index - 1][2]
    else:
        down_fluctuation = fluctuation

    down_price = max(price - down_fluctuation, 0.01)
    up_price = price + fluctuation

    # 確保下限不會高於價格本身
    down_price = min(down_price, price)

    return round(down_price, 2), round(up_price, 2)
