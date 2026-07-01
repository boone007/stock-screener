def calculate_growth_score(fundamentals: dict) -> dict:
    """
    Growth Score (0-20)
    Weights: Revenue Growth 35%, EPS Growth 35%, FCF Growth 30%
    """
    breakdown = {}
    total = 0.0
    max_possible = 0.0

    rev_growth = fundamentals.get("revenue_growth_yoy")
    if rev_growth is not None:
        if rev_growth >= 0.40:
            rev_score = 7.0
        elif rev_growth >= 0.25:
            rev_score = 5.6
        elif rev_growth >= 0.15:
            rev_score = 4.2
        elif rev_growth >= 0.05:
            rev_score = 2.8
        elif rev_growth >= 0:
            rev_score = 1.4
        else:
            rev_score = 0.3
        breakdown["revenue_growth_yoy"] = round(rev_score, 2)
        total += rev_score
        max_possible += 7.0
    else:
        breakdown["revenue_growth_yoy"] = None

    eps_growth = fundamentals.get("eps_growth_yoy")
    if eps_growth is not None:
        if eps_growth >= 0.50:
            eps_score = 7.0
        elif eps_growth >= 0.30:
            eps_score = 5.6
        elif eps_growth >= 0.15:
            eps_score = 4.2
        elif eps_growth >= 0.05:
            eps_score = 2.8
        elif eps_growth >= 0:
            eps_score = 1.4
        else:
            eps_score = 0.3
        breakdown["eps_growth_yoy"] = round(eps_score, 2)
        total += eps_score
        max_possible += 7.0
    else:
        breakdown["eps_growth_yoy"] = None

    fcf_yield = fundamentals.get("fcf_yield")
    if fcf_yield is not None:
        if fcf_yield >= 0.10:
            fcf_score = 6.0
        elif fcf_yield >= 0.06:
            fcf_score = 4.8
        elif fcf_yield >= 0.03:
            fcf_score = 3.6
        elif fcf_yield >= 0:
            fcf_score = 2.0
        else:
            fcf_score = 0.5
        breakdown["fcf_yield"] = round(fcf_score, 2)
        total += fcf_score
        max_possible += 6.0
    else:
        breakdown["fcf_yield"] = None

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
        return "Hyper Growth"
    elif score >= 12:
        return "Strong Growth"
    elif score >= 8:
        return "Moderate Growth"
    elif score >= 4:
        return "Slow Growth"
    return "Declining"
