import yfinance as yf

def get_current_price(stock_code: str) -> float | str:
    try:
        stock = yf.Ticker(stock_code)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        if price is None:
            return f"未找到股票: {stock_code}"
        return float(price)
    except Exception as e:
        return f"获取股票 {stock_code} 价格失败: {str(e)}"


def get_historical_data(stock_code: str, period: str = "1mo") -> dict:
    try:
        stock = yf.Ticker(stock_code)
        hist = stock.history(period=period)
        if hist.empty:
            return {"error": f"未找到股票: {stock_code}"}
        latest = hist.iloc[-1]
        return {
            "stock_code": stock_code,
            "date": str(hist.index[-1].date()),
            "open": float(latest['Open']),
            "high": float(latest['High']),
            "low": float(latest['Low']),
            "close": float(latest['Close']),
            "volume": int(latest['Volume'])
        }
    except Exception as e:
        return {"error": f"获取股票 {stock_code} 历史数据失败: {str(e)}"}


def calculate_investment_return(principal: float, target_value: float) -> float | str:
    if principal <= 0:
        return "错误，本金必须大于零"
    return (target_value / principal - 1) * 100