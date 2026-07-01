def calculate_risk_score(risk_data: dict) -> dict:
    """
    Risk Score (0-20): higher = LOWER risk (safer stock)
    Weights: Beta 25%, Volatility 25%, Altman Z 25%, Debt Ratio 25%
    """
    breakdown = {}
    total = 0.0
    max_possible = 0.0

    beta = risk_data.get("beta")
    if beta is not None:
        abs_beta = abs(beta)
        if abs_beta <= 0.5:
            beta_score = 5.0
        elif abs_beta <= 0.8:
            beta_score = 4.0
        elif abs_beta <= 1.0:
            beta_score = 3.0
        elif abs_beta <= 1.3:
            beta_score = 2.0
        elif abs_beta <= 1.8:
            beta_score = 1.0
        else:
            beta_score = 0.5
        breakdown["beta"] = round(beta_score, 2)
        total += beta_score
        max_possible += 5.0
    else:
        breakdown["beta"] = None

    vol = risk_data.get("volatility_30d")
    if vol is not None:
        if vol <= 0.10:
            vol_score = 5.0
        elif vol <= 0.15:
            vol_score = 4.0
        elif vol <= 0.25:
            vol_score = 3.0
        elif vol <= 0.35:
            vol_score = 2.0
        elif vol <= 0.50:
            vol_score = 1.0
        else:
            vol_score = 0.5
        breakdown["volatility_30d"] = round(vol_score, 2)
        total += vol_score
        max_possible += 5.0
    else:
        breakdown["volatility_30d"] = None

    altman = risk_data.get("altman_z_score")
    if altman is not None:
        if altman >= 3.0:
            z_score = 5.0
        elif altman >= 2.0:
            z_score = 3.5
        elif altman >= 1.23:
            z_score = 2.0
        else:
            z_score = 0.5
        breakdown["altman_z_score"] = round(z_score, 2)
        total += z_score
        max_possible += 5.0
    else:
        breakdown["altman_z_score"] = None

    debt_eq = risk_data.get("debt_to_equity")
    if debt_eq is not None:
        if debt_eq <= 0.1:
            d_score = 5.0
        elif debt_eq <= 0.5:
            d_score = 4.0
        elif debt_eq <= 1.0:
            d_score = 3.0
        elif debt_eq <= 2.0:
            d_score = 2.0
        elif debt_eq <= 3.0:
            d_score = 1.0
        else:
            d_score = 0.5
        breakdown["debt_to_equity"] = round(d_score, 2)
        total += d_score
        max_possible += 5.0
    else:
        breakdown["debt_to_equity"] = None

    if max_possible > 0:
        final = (total / max_possible) * 20.0
    else:
        final = 10.0

    final = min(20.0, max(0.0, final))

    return {
        "score": round(final, 2),
        "breakdown": breakdown,
        "percentile": round((final / 20) * 100, 1),
        "label": _label(final),
    }


def _label(score: float) -> str:
    if score >= 16:
        return "Very Low Risk"
    elif score >= 12:
        return "Low Risk"
    elif score >= 8:
        return "Moderate Risk"
    elif score >= 4:
        return "High Risk"
    return "Very High Risk"
