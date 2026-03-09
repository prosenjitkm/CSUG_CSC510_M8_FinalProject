# Portfolio Essay Outline (2-4 Pages)

Use this structure for your final written submission.

## 1. Problem and Use Case
- Describe the real-world problem: users need help thinking through personal life decisions.
- Explain target users and why transparent reasoning matters.
- State limits: reflective guidance, not legal/medical advice.

## 2. Tools, Libraries, and APIs
- Python, Flask, Flask-CORS.
- Local AI methods:
  - `models.set_operations.Set`
  - `models.sorting.QuickSelect`
  - `models.hash_table.HashTable`
- Standard-library components:
  - `heapq` (A* informed search)
  - `collections.deque` (BFS uninformed search)
  - `re`, `datetime`
- External API:
  - OpenStreetMap Nominatim for geocoding (location -> latitude/longitude).

## 3. Search Methods and Program Goal
- Uninformed search (BFS):
  - Explores symbolic decision states without heuristic guidance.
- Informed search (A*):
  - Uses heuristic distances to prioritize promising states.
- Explain how search helps generate practical step-by-step decision plans.

## 4. Deep Learning Inclusion
- State clearly:
  - This version does not use deep learning.
  - Rationale: rule-based and symbolic methods were chosen for explainability and grading alignment.
- Optional future work: add a classifier model to improve intent detection.

## 5. Expert System Concepts
- Knowledge base:
  - Zodiac profiles, intent keywords, phrase boosts, expert rules.
- Rule inference:
  - Condition -> conclusion rules (e.g., intent=family, element=air, confidence thresholds).
- Explain how rule hits contribute to recommendations.

## 6. Knowledge Representation
- Dictionaries/tables represent:
  - sign traits, intent lexicon, guidance templates, rule base.
- Symbolic graph represents:
  - decision states, actions, transitions, and goal state.

## 7. Symbolic Planning
- Define planning states and goal (`decision_ready`).
- Explain action selection and plan generation.
- Compare BFS and A* node expansion and why selected method is used.

## 8. Results, Limitations, and Future Improvements
- Results:
  - App returns consistent structured guidance and transparent reasoning trace.
- Limitations:
  - Rule-based interpretation can miss nuance.
  - No deep learning or probabilistic uncertainty model.
- Future improvements:
  - richer knowledge base, weighted evidence, model-based intent classifier.

## 9. References (At least 3, APA format)
- Include at least three academic/technical references supporting:
  - expert systems / symbolic AI,
  - search/planning methods (BFS, A*),
  - geocoding API or decision support concepts.
