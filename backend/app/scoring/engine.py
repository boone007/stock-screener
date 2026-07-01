from datetime import datetime, timezone
from .momentum import calculate_momentum_score
from .value import calculate_value_score
from .quality import calculate_quality_score
from .growth import calculate_growth_score
from .risk import calculate_risk_score


GRADE_THRESHOLDS = [
    (90, "A+"), (85, "A"), (80, "A-"),
    (75, "B+"), (70, "B"), (65, "B-"),
    (55, "C+"), (50, "C"), (40, "C-"),
    (30, "D"), (0, "F"),
]


def _grade(score: float) -> str:
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"


def _trend_direction(momentum_score: float, composite: float) -> str:
    if momentum_score >= 13 and composite >= 60:
        return "bullish"
    elif momentum_score <= 7 or composite <= 35:
        return "bearish"
    return "neutral"


def _probabilities(composite: float, momentum: float, risk: float) -> tuple[float, float, float]:
    """
    Probability estimates for directional moves over next 30 days.
    These are data-driven estimates, NOT financial advice.
    """
    bull_raw = (composite * 0.5 + momentum * 2.5 + risk * 1.0) / (50 + 50 + 20)
    bull = max(0.05, min(0.90, bull_raw))
    bear = max(0.05, min(0.90, 1 - bull - 0.10))
    neutral = max(0.05, min(0.90, 1 - bull - bear))

    total = bull + bear + neutral
    return round(bull / total, 3), round(bear / total, 3), round(neutral / total, 3)


class ZenRatingEngine:
    def score(
        self,
        ticker: str,
        company_name: str,
        sector: str,
        industry: str,
        fundamentals: dict,
        technicals: dict,
        risk_data: dict,
        data_source: str = "mock",
    ) -> dict:
        momentum = calculate_momentum_score(technicals)
        value = calculate_value_score(fundamentals)
        quality = calculate_quality_score(fundamentals)
        growth = calculate_growth_score(fundamentals)
        risk = calculate_risk_score(risk_data)

        composite_total = (
            momentum["score"]
            + value["score"]
            + quality["score"]
            + growth["score"]
            + risk["score"]
        )

        trend = _trend_direction(momentum["score"], composite_total)
        bull_prob, bear_prob, neutral_prob = _probabilities(
            composite_total, momentum["score"], risk["score"]
        )

        return {
            "ticker": ticker.upper(),
            "company_name": company_name,
            "sector": sector,
            "industry": industry,
            "momentum": {**momentum},
            "value": {**value},
            "quality": {**quality},
            "growth": {**growth},
            "risk": {**risk},
            "composite": {
                "total": round(composite_total, 2),
                "grade": _grade(composite_total),
                "percentile": round(composite_total, 1),
                "trend": trend,
                "bull_probability": bull_prob,
                "bear_probability": bear_prob,
                "neutral_probability": neutral_prob,
            },
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "data_source": data_source,
        }
