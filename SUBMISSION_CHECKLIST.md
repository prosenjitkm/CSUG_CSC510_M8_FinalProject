# Submission Checklist

## 1. Run Verification
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] CLI starts: `python astrology_ai.py`
- [ ] Web app starts: `python app.py`
- [ ] UI loads at `http://localhost:5000/`

## 2. CLI Test Flow
- [ ] Enter full name
- [ ] Enter gender (`M` or `F`)
- [ ] Enter date of birth
- [ ] Enter time of birth
- [ ] Enter location of birth
- [ ] Ask a question and verify non-error response
- [ ] Type `exit` to close cleanly

## 3. UI Test Flow
- [ ] Full name entered
- [ ] Gender selected from dropdown
- [ ] Date/time/location entered
- [ ] Statement entered
- [ ] Analyze succeeds
- [ ] Reasoning section renders (scores, rules, plan, API details)

## 4. API Validation Checks
- [ ] Missing gender returns `400`
- [ ] Invalid gender returns `400`
- [ ] Valid gender (`male/female` or `M/F`) returns `200`

## 5. Documentation Checks
- [ ] `README_ASTROLOGY.md` reflects current required inputs
- [ ] `ACHIEVEMENT_SUMMARY.md` reflects implemented features
- [ ] `PROJECT_EVALUATION.md` reflects rubric coverage and gaps

## 6. Packaging Checks
- [ ] Include application code and required folders
- [ ] Include `requirements.txt`
- [ ] Include `README_ASTROLOGY.md`
- [ ] Exclude unrelated local/IDE artifacts

## 7. Final Sanity
- [ ] `python -m py_compile app.py astrology_ai.py controllers\\astrology_controller.py`
- [ ] No runtime traceback in normal test path
