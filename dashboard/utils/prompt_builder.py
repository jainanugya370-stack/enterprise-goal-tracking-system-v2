def build_employee_analysis_prompt(employee, goals, updates):

    return f"""
    You are an advanced enterprise HR AI assistant.

    Analyze employee performance professionally.

    EMPLOYEE:
    {employee.username}

    GOALS:
    {goals}

    QUARTERLY UPDATES:
    {updates}

    Generate detailed analysis in this format:

    1. Overall Performance Summary

    2. Productivity Analysis

    3. Goal Completion Quality

    4. Key Strengths

    5. Areas Needing Improvement

    6. Performance Risk Level
       (Low / Medium / High)

    7. Manager Recommendations

    8. Coaching Suggestions

    9. Employee Growth Potential

    Keep the tone professional and enterprise-ready.
    """