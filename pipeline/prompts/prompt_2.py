 
def get_prompt_2(task_description: str) -> str:
    """
    PROMPT 2: SUBTASK DECOMPOSITION
    Follows PRODUCTION_READY_ALL_PROMPTS.md exactly
    """
    return f"""=== PROMPT 2: SUBTASK DECOMPOSITION ===

MAIN TASK: {task_description}

---

Break this task into 5-8 specific subtasks.

For EACH subtask:

1. Subtask name
   - Be specific and concrete

2. Description
   - What does this subtask involve?
   - How long does it typically take?

3. Time spent (%)
   - What % of the total task time?
   - Should sum to 100% across all subtasks

4. Importance (0-1 scale)
   - 0 = Optional, can skip
   - 0.5 = Moderately important
   - 1.0 = Critical, must do

5. AI applicable? (yes/no/partially)
   - Can AI/automation help with this?

6. Why? (Explanation)
   - Explain your answer above

OUTPUT ONLY THIS EXACT JSON (no markdown, no code blocks):

{{
  "main_task": "{task_description}",
  "subtasks": [
    {{
      "id": 1,
      "subtask_name": "Name of subtask",
      "description": "What this subtask involves",
      "time_percent": XX,
      "importance": 0.X,
      "ai_applicable": "yes/no/partially",
      "why": "Explanation"
    }}
  ]
}}

Must have 5-8 subtasks. Time percents must sum to 100%. No markdown. Only JSON."""
