def get_prompt_1(task_description: str, vendor_ctx: str = "") -> str:
    """
    PROMPT 1: VENDOR DISCOVERY (WITH VALIDATION)
    Follows PRODUCTION_READY_ALL_PROMPTS.md exactly
    """
    return f"""=== PROMPT 1: VENDOR DISCOVERY FOR TASK AUTOMATION ===

TASK TO ANALYZE: {task_description}

---
ADDITIONAL CONTEXT FROM REAL-WORLD SOURCES:
{vendor_ctx}
---

You are a technical domain expert doing comprehensive vendor research.

Your goal: Find ALL specific vendor solutions that automate or assist with this task.

CRITICAL INSTRUCTIONS:

1. UNDERSTAND THE TASK
   - What does this task involve?
   - What are the typical subtasks?
   - What are the pain points?

2. SEARCH FOR VENDORS (Search thoroughly)
   - Search vendor documentation
   - Search official product pages
   - Search recent blog posts
   - Look for SPECIFIC product names (not generic AI)
   - Check: GitHub, OpenAI, Anthropic, Google, Amazon, Microsoft, Hugging Face, industry-specific vendors

3. VALIDATE YOUR FINDINGS (This is critical)
   - For each vendor you find:
     a) Check if product actually exists (visit official website)
     b) Verify the name and features match documentation
     c) Confirm the capability matches the task
     d) Find official announcement/evidence link

4. EXTRACT VENDOR DETAILS
   - For EACH vendor/tool found, provide:
     1. Vendor Company Name (official legal name)
     2. Product/Tool Name (exact product name)
     3. What it does (specific technical capability for THIS TASK)
     4. How it replaces/automates the manual work
     5. Official evidence link (product page or blog)
     6. Current Status (commercial, beta, open-source, research)
     7. Domain (specialized/general-purpose)

OUTPUT FORMAT - Create a markdown table:

| Subtask | Vendor Company | Product Name | Capability | What It Replaces | Evidence Link | Status | Domain |
|---------|----------------|--------------|-----------|------------------|---------------|--------|---------|
| [Subtask] | [Company] | [Product] | [Specific capability] | [Manual work removed] | [URL] | [Type] | [Specialized/General] |

RULES:
✅ DO include: Real vendor names, real products, specific capabilities
✅ DO include: Commercial, open-source, and research tools
✅ DO search: All major vendors and domain-specific solutions
✅ DO validate: Each tool actually exists before including

❌ DON'T include: Generic AI assistants unless specifically designed for this task
❌ DON'T guess: Only include tools you can verify
❌ DON'T speculate: Use only official evidence links

OUTPUT ONLY VALID JSON ARRAY (no markdown, no code blocks):
[{{"vendor_company":"Company","product_name":"Product","capability":"Specific capability","what_it_replaces":"Manual work","evidence_link":"https://...","status":"commercial","domain":"specialized"}}]

Include at least 5-8 vendors/tools. Output ONLY valid JSON array."""