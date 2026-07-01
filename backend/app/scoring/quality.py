def calculate_quality_score(fundamentals: dict) -> dict:
    """
    Quality Score (0-20)
    Weights: ROE 25%, ROA 20%, Gross Margin 25%, Operating Margin 15%, Piotroski F-Score 15%
    """
    breakdown = {}
    total = 0.0
    max_possible = 0.0

    roe = fundamentals.get("roe")
    if roe is not None:
        if roe >= 0.30:
            roe_score = 5.0
        elif roe >= 0.20:
            roe_score = 4.0
        elif roe >= 0.15:
            roe_score = 3.0
        elif roe >= 0.10:
            roe_score = 2.0
        elif roe >= 0.05:
            roe_score = 1.0
        else:
            roe_score = 0.5
        breakdown["roe"] = round(roe_score, 2)
        total += roe_score
        max_possible += 5.0
    else:
        breakdown["roe"] = None

    roa = fundamentals.get("roa")
    if roa is not None:
        if roa >= 0.15:
            roa_score = 4.0
        elif roa >= 0.10:
            roa_score = 3.2
        elif roa >= 0.06:
            roa_score = 2.4
        elif roa >= 0.02:
            roa_score = 1.6
        elif roa >= 0:
            roa_score = 0.8
        else:
            roa_score = 0.2
        breakdown["roa"] = round(roa_score, 2)
        total += roa_score
        max_possible += 4.0
    else:
        breakdown["roa"] = None

    gross_margin = fundamentals.get("gross_margin")
    if gross_margin is not None:
        if gross_margin >= 0.60:
            gm_score = 5.0
        elif gross_margin >= 0.40:
            gm_score = 4.0
        elif gross_margin >= 0.30:
            gm_score = 3.0
        elif gross_margin >= 0.20:
            gm_score = 2.0
        elif gross_margin >= 0.10:
            gm_score = 1.0
        else:
            gm_score = 0.5
        breakdown["gross_margin"] = round(gm_score, 2)
        total += gm_score
        max_possible += 5.0
    else:
        breakdown["gross_margin"] = None

    op_margin = fundamentals.get("operating_margin")
    if op_margin is not None:
        if op_margin >= 0.25:
            op_score = 3.0
        elif op_margin >= 0.15:
            op_score = 2.4
        elif op_margin >= 0.08:
            op_score = 1.8
        elif op_margin >= 0:
            op_score = 1.0
        else:
            op_score = 0.3
        breakdown["operating_margin"] = round(op_score, 2)
        total += op_score
        max_possible += 3.0
    else:
        breakdown["operating_margin"] = None

    piotroski = fundamentals.get("piotroski_f_score")
    if piotroski is not None:
        f_score = (piotroski / 9.0) * 3.0
        breakdown["piotroski_f_score"] = round(f_score, 2)
        total += f_score
        max_possible += 3.0
    else:
        breakdown["piotroski_f_score"] = None

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
        return "Exceptional Quality"
    elif score >= 12:
        return "High Quality"
    elif score >= 8:
        return "Average Quality"
    elif score >= 4:
        return "Below Average Quality"
    return "Low Quality"
