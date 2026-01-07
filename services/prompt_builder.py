def build_prompt(student, previous_titles):
    trends = [
        "Security-first backend design",
        "AI-assisted automation",
        "Scalable REST architectures",
        "Analytics and monitoring"
    ]

    return f"""
Generate a COMPLETELY NEW software project idea.

Student Profile:
- Skills: {", ".join(student["skills"])}
- Interest Area: {student["interest_area"]}
- Level: {student["level"]}

Previously Generated Projects (DO NOT repeat):
{previous_titles if previous_titles else "None"}

System Trends (must include at least one):
{", ".join(trends)}

Rules:
- Do NOT repeat or slightly modify previous projects
- Increase complexity compared to typical CRUD apps
- Project must be placement-ready

Return ONLY valid JSON in this structure:
{{
  "title": "",
  "difficulty_level": "",
  "domain": "",
  "tech_stack": [],
  "problem_statement": "",
  "core_features": [],
  "architecture": {{
    "backend": "",
    "database": "",
    "security": ""
  }},
  "industry_trends_used": [],
  "advanced_extensions": [],
  "placement_relevance_score": 0
}}
"""
