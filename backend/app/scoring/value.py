def calculate_value_score(fundamentals: dict) -> dict:
    """
    Value Score (0-20)
    Weights: P/E 30%, P/B 20%, P/S 20%, EV/EBITDA 20%, FCF Yield 10%
    """
    breakdown = {}
    total = 0.0
    max_possible = 0.0

    pe = fundamentals.get("pe_ratio")
    if pe is not None and pe > 0:
        if pe < 10:
            pe_score = 6.0
        elif pe < 15:
            pe_score = 5.0
        elif pe < 20:
            pe_score = 4.0
        elif pe < 25:
            pe_score = 3.0
        elif pe < 35:
            pe_score = 2.0
        elif pe < 50:
            pe_score = 1.0
        else:
            pe_score = 0.5
        breakdown["pe_ratio"] = round(pe_score, 2)
        total += pe_score
        max_possible += 6.0
    else:
        breakdown["pe_ratio"] = None

    pb = fundamentals.get("pb_ratio")
    if pb is not None and pb > 0:
        if pb < 1.0:
            pb_score = 4.0
        elif pb < 2.0:
            pb_score = 3.2
        elif pb < 3.0:
            pb_score = 2.4
        elif pb < 5.0:
            pb_score = 1.6
        elif pb < 10.0:
            pb_score = 0.8
        else:
            pb_score = 0.4
        breakdown["pb_ratio"] = round(pb_score, 2)
        total += pb_score
        max_possible += 4.0
    else:
        breakdown["pb_ratio"] = None

    ps = fundamentals.get("ps_ratio")
    if ps is not None and ps > 0:
        if ps < 1.0:
            ps_score = 4.0
        elif ps < 2.0:
            ps_score = 3.2
        elif ps < 5.0:
            ps_score = 2.4
        elif ps < 10.0:
            ps_score = 1.6
        elif ps < 20.0:
            ps_score = 0.8
        else:
            ps_score = 0.4
        breakdown["ps_ratio"] = round(ps_score, 2)
        total += ps_score
        max_possible += 4.0
    else:
        breakdown["ps_ratio"] = None

    ev_ebitda = fundamentals.get("ev_ebitda")
    if ev_ebitda is not None and ev_ebitda > 0:
        if ev_ebitda < 8:
            evebitda_score = 4.0
        elif ev_ebitda < 12:
            evebitda_score = 3.2
        elif ev_ebitda < 18:
            evebitda_score = 2.4
        elif ev_ebitda < 25:
            evebitda_score = 1.6
        elif ev_ebitda < 40:
            evebitda_score = 0.8
        else:
            evebitda_score = 0.4
        breakdown["ev_ebitda"] = round(evebitda_score, 2)
        total += evebitda_score
        max_possible += 4.0
    else:
        breakdown["ev_ebitda"] = None

    fcf_yield = fundamentals.get("fcf_yield")
    if fcf_yield is not None:
        if fcf_yield > 0.08:
            fcf_score = 2.0
        elif fcf_yield > 0.05:
            fcf_score = 1.6
        elif fcf_yield > 0.02:
            fcf_score = 1.2
        elif fcf_yield > 0:
            fcf_score = 0.8
        else:
            fcf_score = 0.2
        breakdown["fcf_yield"] = round(fcf_score, 2)
        total += fcf_score
        max_possible += 2.0
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
        return "Deep Value"
    elif score >= 12:
        return "Undervalued"
    elif score >= 8:
        return "Fairly Valued"
    elif score >= 4:
        return "Slightly Overvalued"
    return "Overvalued"
