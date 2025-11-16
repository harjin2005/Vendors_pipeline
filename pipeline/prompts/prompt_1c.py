 
def get_prompt_1c(vendor: str, product: str, task: str) -> str:
    """
    PROMPT 1C: FUTURE TIMELINE (2025-2026)
    Follows PRODUCTION_READY_ALL_PROMPTS.md exactly
    """
    return f"""=== PROMPT 1C: FUTURE CAPABILITY ANALYSIS ===

VENDOR: {vendor}
TOOL: {product}
TASK: {task}

---

Analyze what this vendor has ANNOUNCED for the future (2025-2026).

Research and answer:

1. What's on the official roadmap?
   - Check: Official roadmap page, investor presentations, CEO statements
   - List announced features/improvements

2. What new capabilities might come for {task}?
   - How will it improve?
   - What problems will it solve?
   - Specific to this task?

3. Expected timeline?
   - Q1 2025? Q2 2025? Q4 2025? Uncertain?

4. How confident are we?
   - HIGH = Official roadmap, concrete announcements
   - MEDIUM = Stated plans, investor calls
   - LOW = Speculation, industry trends

5. If released, how good could it be? (Rate 0-1)
   - What's the expected improvement?

6. Evidence link (roadmap, press release, research paper)

OUTPUT ONLY THIS EXACT JSON (no markdown, no code blocks):

{{
  "vendor": "{vendor}",
  "tool": "{product}",
  "task": "{task}",
  "timeline_phase": "FUTURE",
  "announced_features": ["Feature 1", "Feature 2"],
  "expected_timeline": "Q? 2025 or Uncertain",
  "confidence_level": "high/medium/low",
  "capability_if_released": "What it could do",
  "aps_score_expected": 0.X,
  "improvement_from_current": "+X%",
  "evidence_url": "https://..."
}}

No markdown. Only JSON."""
