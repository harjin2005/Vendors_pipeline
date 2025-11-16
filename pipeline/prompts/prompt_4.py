 
def get_prompt_4(task: str, capability_mapping_json: str) -> str:
    """
    PROMPT 4: FINAL APS & HRF CALCULATION
    Follows PRODUCTION_READY_ALL_PROMPTS.md exactly
    """
    return f"""=== PROMPT 4: FINAL APS & HRF CALCULATION ===

TASK: {task}

CAPABILITY MAPPING:
{capability_mapping_json}

---

Calculate final scores and generate recommendations.

For EACH vendor:

1. APS (AI Performance Score)
   - Current (2024): Average of all subtask APS scores
   - Future (2025): Based on expected improvements

2. Supporting metrics
   - Adoption rate
   - Maturity (production-ready? yes/no)

Calculate HRF (Human Requirement Factor):

1. Regulatory requirement (0-1)
   - Is this regulated industry?
   - Are there compliance requirements?

2. Trust/verification needed (0-1)
   - Do organizations trust AI decisions?
   - Is human review mandatory?

3. Domain expertise required (0-1)
   - Does this need deep specialist knowledge?
   - Can edge cases occur?

4. Customer impact (0-1)
   - How visible to customers?
   - How costly if wrong?

5. Mission criticality (0-1)
   - Is this mission-critical?
   - Can failures be catastrophic?

Weighted HRF = Average of the 5 components

Final Analysis:

1. Best vendor (current)
   - Which vendor has highest current APS?
   - Why is it best?

2. Task automation percentage (current)
   - What % of task can be automated?
   - Calculate: (Best APS - HRF) / (1 - HRF) × 100%

3. Timeline projections
   - 2024 automation %
   - 2025 automation %
   - 2026 automation %

4. Recommendations
   - Which tools to implement?
   - How should the work be organized?
   - What's the implementation strategy?

OUTPUT ONLY THIS EXACT JSON (no markdown, no code blocks):

{{
  "task": "{task}",
  "vendor_scores": [
    {{
      "vendor": "VENDOR NAME",
      "tool": "TOOL NAME",
      "aps_2024": 0.X,
      "aps_2025": 0.X,
      "adoption_rate": 0.X,
      "maturity": "alpha/beta/production",
      "production_ready": true/false
    }}
  ],
  "hrf_analysis": {{
    "regulatory_requirement": 0.X,
    "trust_verification_needed": 0.X,
    "domain_expertise_required": 0.X,
    "customer_impact": 0.X,
    "mission_criticality": 0.X,
    "weighted_hrf_total": 0.X,
    "interpretation": "X% human still required"
  }},
  "final_analysis": {{
    "best_vendor_current": "VENDOR + TOOL",
    "best_vendor_aps_2024": 0.X,
    "best_vendor_aps_2025": 0.X,
    "task_automation_percent_2024": "X%",
    "task_automation_percent_2025": "X%",
    "task_automation_percent_2026": "X%",
    "automation_trend": "Accelerating/Stable/Slowing",
    "implementation_strategy": "Recommended approach",
    "tools_to_implement": ["Tool 1", "Tool 2"],
    "key_recommendations": "..."
  }}
}}

No markdown. Only JSON."""
