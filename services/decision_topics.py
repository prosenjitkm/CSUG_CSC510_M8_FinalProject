"""
Decision-topic helpers adapted from the CSC510_M8 project.

These utilities provide:
1) topic detection from free-text user statements
2) intent-score boosts from topic matches
3) follow-up question suggestions for clearer decision support
"""

from __future__ import annotations

from typing import Any, Dict, List


TOPIC_HINTS: Dict[str, Dict[str, Any]] = {
    # Career
    "career": {"label": "career decisions", "intent": "career", "factors": ["skills", "timing", "risk"]},
    "job": {"label": "job change", "intent": "career", "factors": ["role fit", "salary", "timing"]},
    "promotion": {"label": "career promotion", "intent": "career", "factors": ["visibility", "results", "timing"]},
    "business": {"label": "business planning", "intent": "career", "factors": ["market", "cash flow", "execution"]},
    "entrepreneur": {"label": "entrepreneurship", "intent": "career", "factors": ["risk", "resources", "timing"]},

    # Love
    "marriage": {"label": "marriage", "intent": "love", "factors": ["values", "communication", "timing"]},
    "marry": {"label": "marriage", "intent": "love", "factors": ["values", "communication", "timing"]},
    "married": {"label": "marriage", "intent": "love", "factors": ["values", "communication", "timing"]},
    "relationship": {"label": "relationship", "intent": "love", "factors": ["trust", "communication", "boundaries"]},
    "partner": {"label": "partnership", "intent": "love", "factors": ["alignment", "trust", "expectations"]},
    "love": {"label": "love and romance", "intent": "love", "factors": ["communication", "security", "timing"]},

    # Money
    "money": {"label": "financial decisions", "intent": "money", "factors": ["budget", "risk", "timeline"]},
    "finance": {"label": "financial planning", "intent": "money", "factors": ["budget", "debt", "goals"]},
    "invest": {"label": "investment decisions", "intent": "money", "factors": ["risk", "liquidity", "horizon"]},
    "loan": {"label": "loan commitment", "intent": "money", "factors": ["interest", "cash flow", "stability"]},
    "debt": {"label": "debt management", "intent": "money", "factors": ["priority", "payments", "discipline"]},
    "house": {"label": "home purchase", "intent": "money", "factors": ["down payment", "cash flow", "timing"]},
    "property": {"label": "property decision", "intent": "money", "factors": ["budget", "location", "timeline"]},

    # Health
    "health": {"label": "health and well-being", "intent": "health", "factors": ["sleep", "stress", "habits"]},
    "stress": {"label": "stress management", "intent": "health", "factors": ["routine", "rest", "support"]},
    "anxiety": {"label": "anxiety management", "intent": "health", "factors": ["support", "coping", "consistency"]},
    "burnout": {"label": "burnout recovery", "intent": "health", "factors": ["recovery", "boundaries", "workload"]},
    "medical": {"label": "medical decisions", "intent": "health", "factors": ["professional advice", "timing", "safety"]},

    # Family
    "baby": {"label": "family planning", "intent": "family", "factors": ["readiness", "support", "timeline"]},
    "pregnancy": {"label": "pregnancy planning", "intent": "family", "factors": ["health", "timing", "support"]},
    "pregnant": {"label": "pregnancy planning", "intent": "family", "factors": ["health", "timing", "support"]},
    "child": {"label": "family planning", "intent": "family", "factors": ["care capacity", "finances", "timing"]},
    "children": {"label": "family planning", "intent": "family", "factors": ["care capacity", "finances", "timing"]},
    "fertility": {"label": "fertility planning", "intent": "family", "factors": ["medical input", "timing", "support"]},
    "family": {"label": "family decision", "intent": "family", "factors": ["alignment", "support", "timeline"]},

    # General
    "this year": {"label": "year planning", "intent": "general", "factors": ["timing", "priorities", "constraints"], "boost": 1},
    "next year": {"label": "year planning", "intent": "general", "factors": ["timing", "priorities", "resources"], "boost": 1},
    "decision": {"label": "important decision", "intent": "general", "factors": ["tradeoffs", "timing", "clarity"]},
}


INTENT_FOLLOWUPS: Dict[str, List[str]] = {
    "career": [
        "What outcome do I want from this career move in the next 12 months?",
        "What is the biggest risk if I act now versus wait?",
        "What one skill gap should I close first?",
    ],
    "love": [
        "What expectation should I communicate clearly before deciding?",
        "What pattern has repeated in my recent relationships?",
        "What timeline feels emotionally and practically realistic?",
    ],
    "money": [
        "What is my hard budget limit for this decision?",
        "How much risk can I tolerate without stress?",
        "What is my time horizon: short, medium, or long term?",
    ],
    "health": [
        "Which daily habit is causing the most stress right now?",
        "What realistic health change can I sustain for 30 days?",
        "When should I involve a qualified professional?",
    ],
    "family": [
        "Are both partners aligned on timing and responsibilities?",
        "What support system is already available for this decision?",
        "What practical milestone should we confirm before acting?",
    ],
    "general": [
        "Which option aligns best with my long-term values?",
        "What is the cost of delaying this decision by 90 days?",
        "What first step can I take within 24 hours?",
    ],
}


def detect_decision_topics(statement: str, limit: int = 3) -> List[Dict[str, Any]]:
    lowered = (statement or "").lower()
    hits: List[Dict[str, Any]] = []

    for keyword, meta in TOPIC_HINTS.items():
        if keyword in lowered:
            base_score = len(keyword.split()) + 1
            if meta.get("intent") == "general":
                base_score -= 1
            hits.append(
                {
                    "keyword": keyword,
                    "label": meta["label"],
                    "intent": meta["intent"],
                    "factors": list(meta.get("factors", [])),
                    "score": base_score,
                }
            )

    # Keep strongest, longer phrase matches first.
    hits.sort(
        key=lambda x: (x.get("intent") != "general", x["score"], len(x["keyword"])),
        reverse=True,
    )
    return hits[:max(1, limit)]


def boost_intent_scores(
    base_scores: Dict[str, int],
    topic_hits: List[Dict[str, Any]],
    boost_per_match: int = 2,
) -> Dict[str, int]:
    boosted = dict(base_scores)
    for hit in topic_hits:
        intent = hit.get("intent")
        if intent:
            boost = int(hit.get("boost", boost_per_match))
            if intent == "general":
                boost = min(boost, 1)
            boosted[intent] = boosted.get(intent, 0) + boost
    return boosted


def follow_up_questions(intent: str, topic_hits: List[Dict[str, Any]]) -> List[str]:
    questions: List[str] = []

    if topic_hits:
        primary = next((h for h in topic_hits if h.get("intent") != "general"), topic_hits[0])
        label = primary.get("label", "this decision")
        factors = primary.get("factors", [])
        if factors:
            questions.append(
                f"For {label}, how will you evaluate {', '.join(factors[:3])}?"
            )

    questions.extend(INTENT_FOLLOWUPS.get(intent, INTENT_FOLLOWUPS["general"]))

    deduped: List[str] = []
    seen = set()
    for q in questions:
        key = q.strip().lower()
        if key and key not in seen:
            seen.add(key)
            deduped.append(q)
        if len(deduped) == 3:
            break
    return deduped
