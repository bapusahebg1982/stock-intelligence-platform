import random


def compute_features(price, history_peak):

    drawdown = ((history_peak - price) / history_peak) * 100

    volatility = random.uniform(1, 5)

    momentum = random.uniform(-2, 3)

    return {
        "drawdown": round(drawdown, 2),
        "volatility": round(volatility, 2),
        "momentum": round(momentum, 2)
    }
