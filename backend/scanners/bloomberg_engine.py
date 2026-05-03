import yfinance as yf
import datetime
from universe.loader import get_us, get_india


# ---------------------------
# 📊 QUANT FEATURES ENGINE
# ---------------------------

def get_metrics(ticker):

    try:
        data = yf.Ticker(ticker).history(period="6mo")

        if data is None or len(data) < 20:
            return None

        close = data["Close"]

        current = close.iloc[-1]
        high = close.max()
        low = close.min()

        drawdown = ((high - current) / high) * 100
        volatility = close.pct_change().std() * 100

        return {
            "price": round(current, 2),
            "drawdown": round(drawdown, 2),
            "volatility": round(volatility, 2),
            "high": round(high, 2),
            "low": round(low, 2)
        }

    except:
        return None


# ---------------------------
# 🧠 SCORING ENGINE (NO AI HERE)
# ---------------------------

def compute_score(m):

    score = 0

    # deeper drawdown = better opportunity (up to a point)
    if m["drawdown"] > 40:
        score += 40
    elif m["drawdown"] > 20:
        score += 25
    else:
        score += 10

    # low volatility = safer bet
    if m["volatility"] < 2:
        score += 25
    elif m["volatility"] < 5:
        score += 15
    else:
        score += 5

    # price stability zone
    if m["price"] > 5:
        score += 10

    return min(score, 100)


# ---------------------------
# 🤖 AI REASONING GENERATOR
# (structured, not free text chaos)
# ---------------------------

def generate_reasoning(stock, metrics):

    reasons = []

    if metrics["drawdown"] > 30:
        reasons.append("Stock is significantly oversold due to market correction")

    if metrics["volatility"] < 3:
        reasons.append("Low volatility indicates stability despite recent price drop")

    if metrics["drawdown"] > 20 and metrics["volatility"] < 4:
        reasons.append("Classic mean-reversion setup observed")

    if len(reasons) == 0:
        reasons.append("Moderate correction with mixed signals")

    opportunity = [
        "Long-term value opportunity if fundamentals remain intact",
        "Potential rebound as valuation normalizes"
    ]

    return {
        "why_down": reasons,
        "why_opportunity": opportunity
    }


# ---------------------------
# 📈 MAIN RANKING ENGINE
# ---------------------------

def run_bloomberg_scan(market="US", max_price=None):

    universe = get_us() if market == "US" else get_india()

    results = []

    for stock in universe:

        m = get_metrics(stock["ticker"])
        if not m:
            continue

        if max_price and m["price"] > float(max_price):
            continue

        score = compute_score(m)

        reasoning = generate_reasoning(stock, m)

        results.append({
            "name": stock["name"],
            "ticker": stock["ticker"],

            # 📊 metrics
            "price": m["price"],
            "drawdown_pct": round(m["drawdown"], 2),
            "volatility": round(m["volatility"], 2),

            # 🧠 ranking
            "score": score,

            # 🤖 AI explanation (structured)
            "reason_drop": reasoning["why_down"],
            "reason_opportunity": reasoning["why_opportunity"],

            "confidence": score
        })

    # 🔥 Bloomberg-style ranking (best first)
    results.sort(key=lambda x: x["score"], reverse=True)

if len(results) == 0:
    return [{
        "name": "Market scanning initializing...",
        "ticker": "N/A",
        "price": 0,
        "drawdown_pct": 0,
        "volatility": 0,
        "score": 0,
        "reason_drop": ["Universe loading or filters too strict"],
        "reason_opportunity": ["Try removing price filter"],
        "confidence": 0
    }]
    
    return results[:25]
