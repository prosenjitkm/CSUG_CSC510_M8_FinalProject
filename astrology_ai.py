"""
Astrology AI Decision Support Assistant

Self-executable CLI program for coursework submission.
Run: python astrology_ai.py
"""

from __future__ import annotations

import re
import heapq
from dataclasses import dataclass
from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from models.hash_table import HashTable
from models.set_operations import Set
from models.sorting import QuickSelect
from services.decision_topics import (
    boost_intent_scores,
    detect_decision_topics,
    follow_up_questions,
)
from services.disclaimers import get_disclosure_payload


@dataclass(frozen=True)
class SignProfile:
    element: str
    modality: str
    ruling_planet: str
    strengths: List[str]
    caution: str


@dataclass(frozen=True)
class UserProfile:
    full_name: str
    date_of_birth: str
    time_of_birth: str
    location_of_birth: str


SIGN_PROFILES: Dict[str, SignProfile] = {
    "aries": SignProfile("fire", "cardinal", "Mars", ["initiative", "courage"], "avoid impulsive commitments"),
    "taurus": SignProfile("earth", "fixed", "Venus", ["stability", "patience"], "avoid resisting needed change"),
    "gemini": SignProfile("air", "mutable", "Mercury", ["adaptability", "communication"], "avoid over-scattering focus"),
    "cancer": SignProfile("water", "cardinal", "Moon", ["empathy", "protection"], "avoid mood-driven decisions"),
    "leo": SignProfile("fire", "fixed", "Sun", ["confidence", "leadership"], "avoid ego-led reactions"),
    "virgo": SignProfile("earth", "mutable", "Mercury", ["analysis", "service"], "avoid perfection paralysis"),
    "libra": SignProfile("air", "cardinal", "Venus", ["balance", "diplomacy"], "avoid indecision for too long"),
    "scorpio": SignProfile("water", "fixed", "Pluto", ["depth", "strategy"], "avoid control-based choices"),
    "sagittarius": SignProfile("fire", "mutable", "Jupiter", ["vision", "optimism"], "avoid overpromising"),
    "capricorn": SignProfile("earth", "cardinal", "Saturn", ["discipline", "planning"], "avoid work-only thinking"),
    "aquarius": SignProfile("air", "fixed", "Uranus", ["innovation", "objectivity"], "avoid emotional detachment"),
    "pisces": SignProfile("water", "mutable", "Neptune", ["intuition", "compassion"], "avoid weak boundaries"),
}

INTENT_KEYWORDS: Dict[str, List[str]] = {
    "career": [
        "job", "career", "work", "promotion", "boss", "team", "interview", "business", "project", "goal",
        "entrepreneur", "company", "market", "resume", "role", "startup", "switch",
    ],
    "love": [
        "love", "relationship", "partner", "dating", "marriage", "married", "romance", "breakup", "trust", "communication",
        "marry", "wife", "husband", "commitment", "engagement",
    ],
    "money": [
        "money", "finance", "salary", "budget", "debt", "spend", "saving", "invest", "purchase", "income",
        "loan", "house", "property", "mortgage", "wealth", "cashflow",
    ],
    "health": [
        "health", "stress", "sleep", "energy", "exercise", "diet", "burnout", "anxiety", "routine", "rest",
        "medical", "therapy", "recovery",
    ],
    "family": [
        "baby", "child", "children", "pregnant", "pregnancy", "conceive", "fertility",
        "family", "parent", "parenting", "mother", "father", "adoption",
    ],
    "general": [
        "decision", "stuck", "confused", "future", "path", "choice", "timing", "direction", "change",
        "plan",
    ],
}

INTENT_PHRASES: Dict[str, List[str]] = {
    "family": [
        "have a baby",
        "start a family",
        "have children",
        "get pregnant",
        "plan a baby",
    ],
    "love": [
        "get married",
        "should i marry",
        "marriage decision",
    ],
}

ELEMENT_GUIDANCE: Dict[str, Dict[str, str]] = {
    "fire": {
        "career": "Act quickly on one high-value opportunity, but verify details before committing.",
        "love": "Lead with honesty and warmth, then slow down to listen before reacting.",
        "money": "Use your confidence to negotiate, but avoid risk decisions made in excitement.",
        "health": "Channel high energy into movement and create a cooldown habit for recovery.",
        "family": "If family planning is the goal, align your energy with a realistic timeline and shared commitments.",
        "general": "Momentum is available now; choose one direction and commit for 2 weeks.",
    },
    "earth": {
        "career": "Build a practical plan with milestones and focus on consistency over speed.",
        "love": "Show care through reliability and clear boundaries rather than assumptions.",
        "money": "Prioritize structure: track expenses and choose sustainable, low-volatility moves.",
        "health": "Stable routines will help most: regular sleep, meals, and manageable exercise.",
        "family": "Create a practical family-readiness plan covering health, support network, and finances.",
        "general": "Ground your next decision in facts, timeline, and concrete trade-offs.",
    },
    "air": {
        "career": "Leverage communication and networking, but reduce distractions to finish key tasks.",
        "love": "Use direct conversation to clarify expectations before making relationship decisions.",
        "money": "Research options widely, then cap analysis time so you actually decide.",
        "health": "Mental overload is the risk; simplify your schedule and protect quiet time.",
        "family": "Discuss expectations openly with your partner and align on values, timing, and responsibilities.",
        "general": "Talk through options, then write a short pros/cons list and decide by deadline.",
    },
    "water": {
        "career": "Trust intuition about people dynamics, then validate with measurable outcomes.",
        "love": "Emotional honesty is your strength; express needs clearly and avoid silent assumptions.",
        "money": "Avoid emotional spending; pause 24 hours before non-essential purchases.",
        "health": "Your system responds to stress quickly; prioritize rest and emotional regulation.",
        "family": "Use emotional clarity and shared values as your base before making major family decisions.",
        "general": "Choose the path that aligns with your values, not just short-term pressure.",
    },
}

MODALITY_GUIDANCE: Dict[str, str] = {
    "cardinal": "You are strongest when initiating action. Start with a clear first step today.",
    "fixed": "You are strongest with persistence. Stay consistent, but be open to one strategic adjustment.",
    "mutable": "You are strongest when adapting. Stay flexible, but keep one non-negotiable priority.",
}

SIGN_ALIASES = {name: name for name in SIGN_PROFILES.keys()}

EXPERT_RULES: List[Dict[str, Any]] = [
    {
        "id": "R1",
        "description": "Family decisions should include partner alignment and practical readiness.",
        "conditions": {"intent": "family"},
        "conclusion": "Include partner alignment, health readiness, and timeline checks before deciding.",
        "weight": 8,
    },
    {
        "id": "R2",
        "description": "Air signs benefit from written analysis plus direct communication.",
        "conditions": {"element": "air"},
        "conclusion": "Use a written pros/cons list and one focused conversation before finalizing.",
        "weight": 7,
    },
    {
        "id": "R3",
        "description": "Low-confidence interpretations should trigger clarification first.",
        "conditions": {"max_confidence": 50},
        "conclusion": "Collect one additional concrete data point before committing.",
        "weight": 7,
    },
    {
        "id": "R4",
        "description": "High-confidence intent match supports immediate action planning.",
        "conditions": {"min_confidence": 75},
        "conclusion": "Convert guidance into a dated 30-day action plan.",
        "weight": 6,
    },
]


def add_edge(graph: Dict[str, List[Dict[str, Any]]], source: str, target: str, action: str, cost: int = 1) -> None:
    graph.setdefault(source, []).append(
        {"to": target, "action": action, "cost": cost}
    )


def build_symbolic_graph(intent: str) -> Dict[str, List[Dict[str, Any]]]:
    graph: Dict[str, List[Dict[str, Any]]] = {}
    add_edge(graph, "start", "clarify_goal", "Clarify your core decision objective.")
    add_edge(graph, "clarify_goal", "collect_facts", "Gather practical facts relevant to the decision.")
    add_edge(graph, "collect_facts", "evaluate_tradeoffs", "Compare trade-offs and constraints.")
    add_edge(graph, "evaluate_tradeoffs", "decision_ready", "Select a path and commit to next steps.")

    if intent == "family":
        add_edge(graph, "start", "partner_alignment", "Discuss family expectations with your partner.")
        add_edge(graph, "partner_alignment", "health_readiness", "Review health readiness with a qualified professional.")
        add_edge(graph, "health_readiness", "financial_readiness", "Check budget and support-network readiness.")
        add_edge(graph, "financial_readiness", "timeline_plan", "Create a 6-12 month timeline with milestones.")
        add_edge(graph, "timeline_plan", "decision_ready", "Decide now or set a review date.")
    elif intent == "career":
        add_edge(graph, "start", "market_scan", "Scan role market and salary benchmarks.")
        add_edge(graph, "market_scan", "skills_gap", "Identify critical skill gaps.")
        add_edge(graph, "skills_gap", "timeline_plan", "Build a transition timeline and risk controls.")
        add_edge(graph, "timeline_plan", "decision_ready", "Commit to apply, wait, or upskill first.")
    elif intent == "money":
        add_edge(graph, "start", "cashflow_review", "Review income, expenses, and liabilities.")
        add_edge(graph, "cashflow_review", "risk_profile", "Determine acceptable risk range.")
        add_edge(graph, "risk_profile", "timeline_plan", "Set financial milestones and review dates.")
        add_edge(graph, "timeline_plan", "decision_ready", "Pick one financial strategy and execute.")
    elif intent == "health":
        add_edge(graph, "start", "symptom_log", "Track sleep, stress, and energy patterns.")
        add_edge(graph, "symptom_log", "professional_check", "Consult a qualified health professional.")
        add_edge(graph, "professional_check", "habit_plan", "Define sustainable habit changes.")
        add_edge(graph, "habit_plan", "decision_ready", "Commit to a health plan and review date.")
    else:
        add_edge(graph, "start", "options_map", "List your top 2-3 options.")
        add_edge(graph, "options_map", "consequence_check", "Estimate likely outcomes for each option.")
        add_edge(graph, "consequence_check", "timeline_plan", "Choose a deadline and execution plan.")
        add_edge(graph, "timeline_plan", "decision_ready", "Decide and take the first action.")

    return graph


def heuristic_distance(state: str) -> int:
    estimates = {
        "start": 4,
        "clarify_goal": 3,
        "collect_facts": 2,
        "evaluate_tradeoffs": 1,
        "options_map": 3,
        "consequence_check": 2,
        "partner_alignment": 3,
        "health_readiness": 2,
        "financial_readiness": 1,
        "market_scan": 3,
        "skills_gap": 2,
        "cashflow_review": 3,
        "risk_profile": 2,
        "symptom_log": 3,
        "professional_check": 2,
        "habit_plan": 1,
        "timeline_plan": 1,
        "decision_ready": 0,
    }
    return estimates.get(state, 4)


def uninformed_bfs_plan(graph: Dict[str, List[Dict[str, Any]]], start: str, goal: str) -> Dict[str, Any]:
    queue = deque([(start, [], [start])])
    visited = {start}
    expanded_order = []

    while queue:
        state, actions, states = queue.popleft()
        expanded_order.append(state)

        if state == goal:
            return {
                "success": True,
                "method": "uninformed_bfs",
                "actions": actions,
                "states": states,
                "nodes_expanded": len(expanded_order),
                "expanded_order": expanded_order,
            }

        for edge in graph.get(state, []):
            nxt = edge["to"]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, actions + [edge["action"]], states + [nxt]))

    return {
        "success": False,
        "method": "uninformed_bfs",
        "actions": [],
        "states": [],
        "nodes_expanded": len(expanded_order),
        "expanded_order": expanded_order,
    }


def informed_a_star_plan(graph: Dict[str, List[Dict[str, Any]]], start: str, goal: str) -> Dict[str, Any]:
    frontier = [(heuristic_distance(start), 0, start, [], [start])]
    best_cost = {start: 0}
    expanded_order = []

    while frontier:
        f_score, g_score, state, actions, states = heapq.heappop(frontier)
        expanded_order.append(state)

        if state == goal:
            return {
                "success": True,
                "method": "informed_a_star",
                "actions": actions,
                "states": states,
                "nodes_expanded": len(expanded_order),
                "expanded_order": expanded_order,
                "path_cost": g_score,
                "f_score": f_score,
            }

        for edge in graph.get(state, []):
            nxt = edge["to"]
            next_g = g_score + int(edge.get("cost", 1))
            if next_g < best_cost.get(nxt, 10 ** 9):
                best_cost[nxt] = next_g
                next_f = next_g + heuristic_distance(nxt)
                heapq.heappush(
                    frontier,
                    (next_f, next_g, nxt, actions + [edge["action"]], states + [nxt]),
                )

    return {
        "success": False,
        "method": "informed_a_star",
        "actions": [],
        "states": [],
        "nodes_expanded": len(expanded_order),
        "expanded_order": expanded_order,
    }


def symbolic_plan_for_intent(intent: str) -> Dict[str, Any]:
    graph = build_symbolic_graph(intent)
    start = "start"
    goal = "decision_ready"
    bfs_result = uninformed_bfs_plan(graph, start, goal)
    a_star_result = informed_a_star_plan(graph, start, goal)

    selected = a_star_result if a_star_result.get("success") else bfs_result

    return {
        "goal": goal,
        "selected_method": selected.get("method"),
        "selected_plan_actions": selected.get("actions", []),
        "selected_plan_states": selected.get("states", []),
        "uninformed_bfs": bfs_result,
        "informed_a_star": a_star_result,
    }


def evaluate_expert_rules(intent: str, element: str, confidence: int) -> List[Dict[str, Any]]:
    triggered: List[Dict[str, Any]] = []
    for rule in EXPERT_RULES:
        conditions = rule.get("conditions", {})
        ok = True
        if "intent" in conditions and conditions["intent"] != intent:
            ok = False
        if "element" in conditions and conditions["element"] != element:
            ok = False
        if "max_confidence" in conditions and confidence > int(conditions["max_confidence"]):
            ok = False
        if "min_confidence" in conditions and confidence < int(conditions["min_confidence"]):
            ok = False
        if ok:
            triggered.append(rule)
    return triggered


def parse_birthdate(date_text: str) -> Optional[datetime]:
    candidate = (date_text or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(candidate, fmt)
        except ValueError:
            continue
    return None


def parse_birthtime(time_text: str) -> Optional[datetime]:
    candidate = (time_text or "").strip().upper()
    for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p"):
        try:
            return datetime.strptime(candidate, fmt)
        except ValueError:
            continue
    return None


def normalize_birthdate(date_text: str) -> Optional[str]:
    parsed = parse_birthdate(date_text)
    if not parsed:
        return None
    return parsed.strftime("%Y-%m-%d")


def normalize_birthtime(time_text: str) -> Optional[str]:
    parsed = parse_birthtime(time_text)
    if not parsed:
        return None
    return parsed.strftime("%H:%M")


def zodiac_from_birthdate(date_text: str) -> Optional[str]:
    dob = parse_birthdate(date_text)
    if not dob:
        return None

    month_day = (dob.month, dob.day)
    if (month_day >= (3, 21)) and (month_day <= (4, 19)):
        return "aries"
    if (month_day >= (4, 20)) and (month_day <= (5, 20)):
        return "taurus"
    if (month_day >= (5, 21)) and (month_day <= (6, 20)):
        return "gemini"
    if (month_day >= (6, 21)) and (month_day <= (7, 22)):
        return "cancer"
    if (month_day >= (7, 23)) and (month_day <= (8, 22)):
        return "leo"
    if (month_day >= (8, 23)) and (month_day <= (9, 22)):
        return "virgo"
    if (month_day >= (9, 23)) and (month_day <= (10, 22)):
        return "libra"
    if (month_day >= (10, 23)) and (month_day <= (11, 21)):
        return "scorpio"
    if (month_day >= (11, 22)) and (month_day <= (12, 21)):
        return "sagittarius"
    if (month_day >= (12, 22)) and (month_day <= (12, 31)):
        return "capricorn"
    if (month_day >= (1, 1)) and (month_day <= (1, 19)):
        return "capricorn"
    if (month_day >= (1, 20)) and (month_day <= (2, 18)):
        return "aquarius"
    return "pisces"


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def detect_sign(text: str) -> Optional[str]:
    tokens = tokenize(text)
    token_set = set(tokens)
    for sign in SIGN_ALIASES:
        if sign in token_set:
            return sign
    return None


def intent_overlap_scores(tokens: List[str]) -> Dict[str, int]:
    user_set = Set(tokens)
    scores: Dict[str, int] = {}
    for intent, words in INTENT_KEYWORDS.items():
        keyword_set = Set(words)
        overlap = user_set.intersection(keyword_set)
        scores[intent] = int(overlap.get("size", 0))
    return scores


def detect_intent(
    statement: str,
    topic_hits: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[str, int, Dict[str, int]]:
    lowered = statement.lower()
    tokens = tokenize(statement)
    scores = intent_overlap_scores(tokens)
    if topic_hits:
        scores = boost_intent_scores(scores, topic_hits, boost_per_match=2)

    for intent, phrases in INTENT_PHRASES.items():
        for phrase in phrases:
            if phrase in lowered:
                scores[intent] = scores.get(intent, 0) + 2

    best_intent = "general"
    best_score = scores.get("general", 0)
    for intent, score in scores.items():
        if score > best_score:
            best_intent = intent
            best_score = score

    if best_score <= 0:
        confidence = 35
    else:
        confidence = min(95, 45 + best_score * 12)

    return best_intent, confidence, scores


def top_factors(
    intent: str,
    tokens: List[str],
    topic_hits: Optional[List[Dict[str, Any]]] = None,
    k: int = 3,
) -> List[str]:
    keyword_pool = set(INTENT_KEYWORDS.get(intent, []))
    matched = [t for t in tokens if t in keyword_pool]
    if topic_hits:
        for hit in topic_hits:
            if hit.get("intent") == intent:
                matched.extend(hit.get("factors", []))

    if not matched:
        defaults = {
            "family": ["timing", "health readiness", "financial readiness"],
            "health": ["sleep", "stress", "routine"],
            "money": ["budget", "risk", "consistency"],
            "love": ["communication", "trust", "timing"],
            "career": ["opportunity", "skills", "timing"],
            "general": ["timing", "priorities", "communication"],
        }
        return defaults.get(intent, defaults["general"])
    unique = []
    seen = set()
    for word in matched:
        if word not in seen:
            seen.add(word)
            unique.append(word)
    return unique[:k]


def quickselect_top_k(pairs: List[Tuple[str, int]], k: int) -> List[Tuple[str, int]]:
    if not pairs:
        return []
    if k >= len(pairs):
        return sorted(pairs, key=lambda x: x[1], reverse=True)

    negatives = [-score for _, score in pairs]
    selector = QuickSelect(negatives)
    kth = selector.find_kth_smallest(k)
    threshold = kth["kth_smallest"] if kth.get("success") else sorted(negatives)[k - 1]

    selected = [(msg, score) for msg, score in pairs if -score <= threshold]
    selected = sorted(selected, key=lambda x: x[1], reverse=True)
    return selected[:k]


def build_recommendation_pool(
    sign: str,
    intent: str,
    tokens: List[str],
    topic_hits: Optional[List[Dict[str, Any]]] = None,
    expert_rule_hits: Optional[List[Dict[str, Any]]] = None,
) -> List[Tuple[str, int]]:
    profile = SIGN_PROFILES[sign]
    factors = top_factors(intent, tokens, topic_hits=topic_hits, k=4)

    pool = [
        (
            f"{profile.element.title()}-element advice: "
            f"{ELEMENT_GUIDANCE[profile.element][intent]}",
            7,
        ),
        (
            f"{profile.modality.title()}-modality note: "
            f"{MODALITY_GUIDANCE[profile.modality]}",
            6,
        ),
        (
            f"Strength leverage: use your {profile.strengths[0]} and {profile.strengths[1]} on this decision.",
            5,
        ),
        (
            f"Caution area: {profile.caution}.",
            6,
        ),
        (
            f"Factor focus now: {', '.join(factors[:3])}.",
            4 + min(3, len(factors)),
        ),
        (
            "Decision rule: choose the option you can sustain for 30 days, not just 3 days.",
            5,
        ),
    ]

    for rule in expert_rule_hits or []:
        pool.append((f"Expert rule {rule['id']}: {rule['conclusion']}", int(rule.get("weight", 6))))

    return pool


def build_recommendations(
    sign: str,
    intent: str,
    tokens: List[str],
    topic_hits: Optional[List[Dict[str, Any]]] = None,
    expert_rule_hits: Optional[List[Dict[str, Any]]] = None,
) -> List[str]:
    message_pool = build_recommendation_pool(
        sign,
        intent,
        tokens,
        topic_hits=topic_hits,
        expert_rule_hits=expert_rule_hits,
    )
    top = quickselect_top_k(message_pool, 3)
    return [item[0] for item in top]


def session_pattern(memory: HashTable) -> Optional[str]:
    items = memory.get_all_items()
    if not items:
        return None
    top_intent, top_count = max(items, key=lambda x: x[1])
    if int(top_count) <= 1:
        return None
    return f"Session pattern: you ask about {top_intent} most often ({top_count} times)."


def update_intent_memory(memory: HashTable, intent: str) -> None:
    existing = memory.get(intent)
    count = 0
    if existing.get("success"):
        try:
            count = int(existing["value"])
        except (TypeError, ValueError):
            count = 0
    memory.insert(intent, count + 1)


def build_analysis(
    statement: str,
    sign: str,
    memory: HashTable,
    user_profile: Optional[UserProfile] = None,
    sign_source: str = "unknown",
    external_api_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    tokens = tokenize(statement)
    topic_hits = detect_decision_topics(statement, limit=3)
    intent, confidence, raw_scores = detect_intent(statement, topic_hits=topic_hits)
    profile = SIGN_PROFILES[sign]
    expert_rule_hits = evaluate_expert_rules(intent, profile.element, confidence)
    matched_factors = top_factors(intent, tokens, topic_hits=topic_hits, k=3)
    recommendation_pool = build_recommendation_pool(
        sign,
        intent,
        tokens,
        topic_hits=topic_hits,
        expert_rule_hits=expert_rule_hits,
    )
    selected_pairs = quickselect_top_k(recommendation_pool, 3)
    symbolic_plan = symbolic_plan_for_intent(intent)
    followups = follow_up_questions(intent, topic_hits)
    disclosures = get_disclosure_payload()

    update_intent_memory(memory, intent)
    pattern = session_pattern(memory)
    today = datetime.now().strftime("%B %d, %Y")

    external_api = external_api_result or {
        "used": False,
        "success": False,
        "details": (
            "No external geolocation/astrology API is called. "
            "Location is stored and displayed as user-provided text only."
        ),
    }

    libraries_and_modules = [
        "models.set_operations.Set for keyword-overlap intent scoring",
        "models.sorting.QuickSelect for top recommendation ranking",
        "models.hash_table.HashTable for per-session topic memory",
        "services.decision_topics for topic-detection score boosts and follow-up prompts",
        "services.disclaimers for ethics/privacy/source transparency notices",
        "collections.deque for uninformed BFS symbolic planning",
        "heapq for informed A* symbolic planning",
        "Python datetime for date/time normalization and zodiac-by-date mapping",
        "Python regex tokenization for statement parsing",
    ]
    if external_api.get("used"):
        libraries_and_modules.append(
            "services.geocoding.geocode_with_nominatim (urllib) for external location -> latitude/longitude lookup"
        )

    pipeline_steps = [
        "Normalize user profile fields (date/time).",
        "Determine sign source: explicit sign, sign in statement, or zodiac from birth date.",
        "Detect decision topics from statement phrases and map them to decision intents.",
        "Tokenize statement with regex.",
        "Boost intent scores using matched decision-topic hints.",
        "Apply expert-system rules over intent, sign element, and confidence.",
        "Compute overlap score between statement tokens and each intent keyword set.",
        "Choose highest-scoring intent and map score to confidence.",
        "Generate symbolic decision plan and search for best path (BFS and A*).",
        "Generate recommendation pool from sign element + modality + caution rules.",
        "Select top 3 recommendations via QuickSelect-based ranking.",
        "Generate follow-up questions to reduce ambiguity in next user turn.",
        "Update session memory using hash-table counters.",
    ]
    if external_api.get("used"):
        pipeline_steps.insert(
            2,
            "Call external geocoding API (OpenStreetMap Nominatim) to convert birth location into latitude/longitude.",
        )

    return {
        "date": today,
        "statement": statement,
        "tokens": tokens,
        "sign": sign,
        "sign_source": sign_source,
        "profile": {
            "element": profile.element,
            "modality": profile.modality,
            "ruling_planet": profile.ruling_planet,
            "strengths": profile.strengths,
            "caution": profile.caution,
        },
        "knowledge_representation": {
            "symbol_tables": [
                "SIGN_PROFILES",
                "INTENT_KEYWORDS",
                "INTENT_PHRASES",
                "ELEMENT_GUIDANCE",
                "MODALITY_GUIDANCE",
                "EXPERT_RULES",
                "services.decision_topics.TOPIC_HINTS",
            ],
            "planning_graph_type": "State-action symbolic graph",
            "memory_store": "HashTable per session",
        },
        "intent": intent,
        "confidence": confidence,
        "signal_scores": raw_scores,
        "decision_topics": topic_hits,
        "matched_factors": matched_factors,
        "expert_rule_hits": expert_rule_hits,
        "symbolic_plan": symbolic_plan,
        "recommendation_pool": [
            {"message": msg, "score": score} for msg, score in recommendation_pool
        ],
        "selected_recommendations": [
            {"rank": i + 1, "message": msg, "score": score}
            for i, (msg, score) in enumerate(selected_pairs)
        ],
        "session_pattern": pattern,
        "follow_up_questions": followups,
        "disclosures": disclosures,
        "external_api": external_api,
        "libraries_and_modules": libraries_and_modules,
        "pipeline_steps": pipeline_steps,
        "user_profile": user_profile,
    }


def format_analysis_text(analysis: Dict[str, Any]) -> str:
    sign = analysis["sign"]
    profile = analysis["profile"]
    user_profile = analysis.get("user_profile")
    score_line = ", ".join(f"{k}:{v}" for k, v in analysis["signal_scores"].items())
    recommendations = analysis["selected_recommendations"]
    symbolic_plan = analysis.get("symbolic_plan", {})
    external_api = analysis.get("external_api", {})
    topic_hits = analysis.get("decision_topics", [])
    disclosures = analysis.get("disclosures", {})
    coordinates = (external_api.get("coordinates") or {}) if external_api else {}

    lines = [
        f"Date: {analysis['date']}",
    ]

    if user_profile:
        lines.extend(
            [
                f"User: {user_profile.full_name}",
                f"Birth details: {user_profile.date_of_birth} at {user_profile.time_of_birth}, {user_profile.location_of_birth}",
            ]
        )

    lines.extend(
        [
        f"Detected sign: {sign.title()} ({profile['element'].title()} / {profile['modality'].title()}, ruled by {profile['ruling_planet']})",
        (
            f"Birth-location coordinates: {coordinates.get('latitude')}, {coordinates.get('longitude')}"
            if coordinates
            else "Birth-location coordinates: unavailable"
        ),
        f"Detected focus: {analysis['intent'].title()} (confidence {analysis['confidence']}%)",
        f"Signal scores: {score_line}",
        (
            "Detected decision topics: "
            + ", ".join(f"{hit.get('label')} ({hit.get('keyword')})" for hit in topic_hits)
            if topic_hits
            else "Detected decision topics: none"
        ),
        (
            "Suggested decision path: "
            + " -> ".join(symbolic_plan.get("selected_plan_actions", [])[:4])
            if symbolic_plan.get("selected_plan_actions")
            else "Suggested decision path: unavailable"
        ),
        "Recommended guidance:",
        f"1. {recommendations[0]['message']}",
        f"2. {recommendations[1]['message']}",
        f"3. {recommendations[2]['message']}",
        "Next action: pick one recommendation and apply it in the next 24 hours.",
        ]
    )

    if analysis["intent"] in {"family", "health"}:
        lines.append("Note: This is reflective guidance and not medical advice.")

    if disclosures.get("short_disclaimer"):
        lines.append(f"Disclaimer: {disclosures['short_disclaimer']}")

    if analysis["session_pattern"]:
        lines.append(analysis["session_pattern"])

    return "\n".join(lines)


def make_response(
    statement: str,
    sign: str,
    memory: HashTable,
    user_profile: Optional[UserProfile] = None,
    sign_source: str = "unknown",
    external_api_result: Optional[Dict[str, Any]] = None,
) -> str:
    analysis = build_analysis(
        statement=statement,
        sign=sign,
        memory=memory,
        user_profile=user_profile,
        sign_source=sign_source,
        external_api_result=external_api_result,
    )
    return format_analysis_text(analysis)


def resolve_sign(user_text: str, date_of_birth: str = "") -> Optional[str]:
    sign = detect_sign(user_text)
    if sign:
        return sign

    from_dob = zodiac_from_birthdate(date_of_birth)
    if from_dob:
        return from_dob

    sign_input = input(
        "I did not detect your zodiac sign. Enter one (Aries..Pisces) or press Enter to continue as General: "
    ).strip().lower()
    if not sign_input:
        return "libra"
    if sign_input in SIGN_PROFILES:
        return sign_input
    return None


def run_cli() -> None:
    disclosures = get_disclosure_payload()

    print("Astrology AI Decision Support Assistant")
    print("Please enter your profile details first, then ask your question.")
    print(f"Note: {disclosures['short_disclaimer']}")
    print("Type 'exit' to quit.\n")

    full_name = input("Full name: ").strip()
    while not full_name:
        print("Full name is required.")
        full_name = input("Full name: ").strip()

    date_of_birth = input("Date of birth (YYYY-MM-DD or MM/DD/YYYY): ").strip()
    normalized_dob = normalize_birthdate(date_of_birth)
    while not normalized_dob:
        print("Invalid date format. Use YYYY-MM-DD or MM/DD/YYYY.")
        date_of_birth = input("Date of birth (YYYY-MM-DD or MM/DD/YYYY): ").strip()
        normalized_dob = normalize_birthdate(date_of_birth)

    time_of_birth = input("Time of birth (24h HH:MM or hh:mm AM/PM): ").strip()
    normalized_tob = normalize_birthtime(time_of_birth)
    while not normalized_tob:
        print("Invalid time format. Use HH:MM (24h) or hh:mm AM/PM.")
        time_of_birth = input("Time of birth (24h HH:MM or hh:mm AM/PM): ").strip()
        normalized_tob = normalize_birthtime(time_of_birth)

    location_of_birth = input("Location of birth (City, Country): ").strip()
    while not location_of_birth:
        print("Location of birth is required.")
        location_of_birth = input("Location of birth (City, Country): ").strip()

    user_profile = UserProfile(
        full_name=full_name,
        date_of_birth=normalized_dob,
        time_of_birth=normalized_tob,
        location_of_birth=location_of_birth,
    )

    memory = HashTable(size=16)

    while True:
        user_text = input("You (your question): ").strip()
        if not user_text:
            print("Please enter a statement or question.\n")
            continue
        if user_text.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if user_text.lower() in {"help", "examples"}:
            print("Examples:")
            print("- Should I switch my job this year?")
            print("- Should I get married this year?")
            print("- Should I have a baby this year?\n")
            continue
        if user_text.lower() in {"disclaimer", "privacy"}:
            print(disclosures["main_disclaimer"])
            print(disclosures["data_privacy_notice"] + "\n")
            continue

        sign = resolve_sign(user_text, user_profile.date_of_birth)
        if sign is None:
            print("Could not recognize that sign. Try again with a valid zodiac name.\n")
            continue

        try:
            response = make_response(user_text, sign, memory, user_profile=user_profile)
            print("\nAstrology AI:\n" + response + "\n")
        except Exception as exc:
            print(f"Astrology AI encountered an error but recovered: {exc}")
            print("Please rephrase your question and try again.\n")


if __name__ == "__main__":
    run_cli()
