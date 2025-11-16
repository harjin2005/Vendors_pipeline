def get_prompt_3(task: str, vendors_json: str, subtasks_json: str) -> str:
    """
    PROMPT 3: CAPABILITY MAPPING WITH TIMELINE
    FINAL PRODUCTION VERSION - Clean and simple
    """
    return f"""You are an expert at analyzing vendor capabilities.

MAIN TASK: {task}

VENDOR DATA:
{vendors_json}

SUBTASKS:
{subtasks_json}

---

Create a comprehensive capability mapping analysis.

For EACH vendor/tool in the vendor data:
1. Determine which subtasks it can handle (yes/no/partially)
2. Generate APS scores for 2024, 2025, and 2026 (each between 0.0 and 1.0)
3. Provide the result using EXACTLY this JSON structure.

CRITICAL INSTRUCTIONS:
- RETURN ONLY VALID JSON
- NO MARKDOWN
- NO CODE BLOCKS
- NO EXPLANATIONS
- NO TEXT BEFORE OR AFTER
- Use regular curly braces and square brackets for JSON
- Start response with opening curly brace
- End response with closing curly brace

EXAMPLE OUTPUT:
{chr(123)}
  "capability_analysis": [
    {chr(123)}
      "vendor": "TestRail, Inc.",
      "tool": "TestRail",
      "subtask_coverage": [
        {chr(123)}
          "subtask": "Identify vendors",
          "can_handle": "yes",
          "aps_2024": 0.75,
          "aps_2025": 0.85,
          "aps_2026": 0.9
        {chr(125)}
      ]
    {chr(125)}
  ]
{chr(125)}

RESPONSE FORMAT:
{chr(123)}
  "capability_analysis": [
    {chr(123)}
      "vendor": "VENDOR_NAME",
      "tool": "TOOL_NAME",
      "subtask_coverage": [
        {chr(123)}
          "subtask": "Subtask name",
          "can_handle": "yes/no/partially",
          "aps_2024": 0.X,
          "aps_2025": 0.X,
          "aps_2026": 0.X
        {chr(125)}
      ]
    {chr(125)}
  ]
{chr(125)}

REQUIREMENTS:
- "capability_analysis" MUST be an array with all vendors
- Each vendor MUST have "vendor", "tool", and "subtask_coverage"
- "subtask_coverage" MUST be an array of objects
- All aps_* values MUST be decimals between 0.0 and 1.0
- If unable to generate, return empty: {chr(123)}"capability_analysis": [{chr(125)}]
"""