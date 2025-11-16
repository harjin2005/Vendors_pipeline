 
def get_prompt_1a(vendor: str, product: str, task: str) -> str:
    """
    PROMPT 1A: PAST TIMELINE (2022-2023)
    Follows PRODUCTION_READY_ALL_PROMPTS.md exactly
    """
    return f"""=== PROMPT 1A: PAST CAPABILITY ANALYSIS ===

VENDOR: {vendor}
TOOL: {product}
TASK: {task}

---

Analyze what this tool could do for this task in 2022-2023 (PAST).

Research and answer:

1. Did this tool exist in 2022?
   - YES / NO
   - If yes, what year was it first launched?

2. What could it do for {task} back in 2022-2023?
   - Describe the capability level
   - What specific features existed?
   - What was it limited in?

3. How good was it? (Rate on 0-1 scale)
   - 0 = Didn't exist
   - 0.3 = Very basic, unreliable
   - 0.5 = Decent but with limitations
   - 0.7 = Good but not production-ready
   - 0.9 = Production-ready, widely used
   - 1.0 = Excellent, industry standard

4. Evidence link (if available)
   - Old blog posts, archived pages, GitHub history
   - Link to documentation from that time period

OUTPUT ONLY THIS EXACT JSON (no markdown, no code blocks):

{{
  "vendor": "{vendor}",
  "tool": "{product}",
  "task": "{task}",
  "timeline_phase": "PAST",
  "year_launched": 20XX or "unknown",
  "existed_in_2022": true/false,
  "capability_in_2023": "Description of what it could do",
  "limitations_2023": "What it couldn't do or was limited in",
  "aps_score_2023": 0.X,
  "evidence_url": "link or N/A"
}}

No markdown. Only JSON."""
