def calculate_momentum_score(technicals: dict) -> dict:
    """
    Momentum Score (0-20)
    Weights: RSI 25%, Price/SMA50 25%, Price/SMA200 20%, Volume Trend 15%, MACD 15%
    """
    breakdown = {}
    total = 0.0

    rsi = technicals.get("rsi_14", 50)
    if rsi >= 70:
        rsi_score = 5.0
    elif rsi >= 60:
        rsi_score = 4.0
    elif rsi >= 50:
        rsi_score = 3.0
    elif rsi >= 40:
        rsi_score = 2.0
    elif rsi >= 30:
        rsi_score = 1.0
    else:
        rsi_score = 0.5
    breakdown["rsi"] = round(rsi_score, 2)
    total += rsi_score * 1.0

    price = technicals.get("current_price", 100)
    sma_50 = technicals.get("sma_50", price)
    if sma_50 and sma_50 > 0:
        ratio_50 = price / sma_50
        if ratio_50 >= 1.10:
            sma50_score = 5.0
        elif ratio_50 >= 1.05:
            sma50_score = 4.0
        elif ratio_50 >= 1.00:
            sma50_score = 3.0
        elif ratio_50 >= 0.95:
            sma50_score = 2.0
        else:
            sma50_score = 1.0
    else:
        sma50_score = 2.5
    breakdown["price_vs_sma50"] = round(sma50_score, 2)
    total += sma50_score * 1.0

    sma_200 = technicals.get("sma_200", price)
    if sma_200 and sma_200 > 0:
        ratio_200 = price / sma_200
        if ratio_200 >= 1.15:
            sma200_score = 4.0
        elif ratio_200 >= 1.05:
            sma200_score = 3.2
        elif ratio_200 >= 1.00:
            sma200_score = 2.4
        elif ratio_200 >= 0.90:
            sma200_score = 1.6
        else:
            sma200_score = 0.8
    else:
        sma200_score = 2.0
    breakdown["price_vs_sma200"] = round(sma200_score, 2)
    total += sma200_score * 0.8

    vol_ratio = technicals.get("volume_ratio", 1.0)
    price_change = technicals.get("price_change_pct_1d", 0)
    if vol_ratio >= 1.5 and price_change > 0:
        vol_score = 3.0
    elif vol_ratio >= 1.2 and price_change > 0:
        vol_score = 2.4
    elif vol_ratio >= 0.8:
        vol_score = 1.8
    elif vol_ratio >= 0.5 and price_change < 0:
        vol_score = 1.2
    else:
        vol_score = 0.6
    breakdown["volume_trend"] = round(vol_score, 2)
    total += vol_score * 0.6

    macd = technicals.get("macd", 0)
    macd_signal = technicals.get("macd_signal", 0)
    macd_hist = technicals.get("macd_histogram", 0)
    if macd > macd_signal and macd_hist > 0:
        macd_score = 3.0
    elif macd > macd_signal:
        macd_score = 2.2
    elif macd_hist > 0:
        macd_score = 1.8
    elif macd < macd_signal and macd_hist < 0:
        macd_score = 0.6
    else:
        macd_score = 1.2
    breakdown["macd"] = round(macd_score, 2)
    total += macd_score * 0.6

    final = min(20.0, max(0.0, total))

    return {
        "score": round(final, 2),
        "breakdown": breakdown,
        "percentile": round((final / 20) * 100, 1),
        "label": _label(final),
    }


def _label(score: float) -> str:
    if score >= 16:
        return "Strong Momentum"
    elif score >= 12:
        return "Positive Momentum"
    elif score >= 8:
        return "Neutral Momentum"
    elif score >= 4:
        return "Weak Momentum"
    return "Negative Momentum"
