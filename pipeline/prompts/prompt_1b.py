 
def get_prompt_1b(vendor: str, product: str, task: str) -> str:
    """
    PROMPT 1B: PRESENT TIMELINE (2024-2025)
    Follows PRODUCTION_READY_ALL_PROMPTS.md exactly
    """
    return f"""=== PROMPT 1B: PRESENT CAPABILITY ANALYSIS ===

VENDOR: {vendor}
TOOL: {product}
TASK: {task}

---

Analyze what this tool can do RIGHT NOW (2024-2025) for {task}.

Research and answer:

1. What new features were added in 2024?
   - List recent feature releases
   - Check official blog and release notes

2. What can it currently do for {task}?
   - Be specific about capabilities
   - What works well? What doesn't?
   - Any known limitations?

3. How good is it NOW? (Rate 0-1 scale)
   - Consider current capabilities, stability, adoption

4. How widely adopted is it? (Rate 0-1 scale)
   - 0 = Nobody uses it
   - 0.3 = Niche usage
   - 0.6 = Growing adoption
   - 0.8 = Mainstream
   - 1.0 = Industry standard

5. Is it production-ready?
   - YES / NO
   - Evidence: Enterprise customers using it? Support available? Stable releases?

6. Latest announcement/blog link
   - Most recent update or release announcement

OUTPUT ONLY THIS EXACT JSON (no markdown, no code blocks):

{{
  "vendor": "{vendor}",
  "tool": "{product}",
  "task": "{task}",
  "timeline_phase": "PRESENT",
  "latest_update_date": "YYYY-MM",
  "new_features_2024": ["Feature 1", "Feature 2", "Feature 3"],
  "current_capability": "Detailed description of what it can do NOW",
  "known_limitations": "What it still can't do or does poorly",
  "aps_score_current": 0.X,
  "adoption_rate": 0.X,
  "production_ready": true/false,
  "enterprise_customers": true/false,
  "latest_announcement_url": "https://..."
}}

No markdown. Only JSON."""
