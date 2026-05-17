from goals.models import Goal, GoalUpdate
from django.db.models import Avg
import requests
from django.conf import settings
import google.generativeai as genai

def generate_ai_insights(prompt):

    try:

        # LOCAL OLLAMA
        if settings.OLLAMA_ENABLED:

            response = requests.post(

                "http://localhost:11434/api/generate",

                json={
                    "model": "phi3:mini",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 300,
                        "temperature": 0.7
                    }
                },

                timeout=180

            )

            if response.status_code != 200:
                return "AI service unavailable."

            data = response.json()
            return data.get("response", "")

        # PRODUCTION GEMINI
        else:

            genai.configure(api_key=settings.GEMINI_API_KEY)

            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(prompt)

            return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


def generate_employee_insight(employee):

    goals = Goal.objects.filter(employee=employee)[:3]

    total_goals = goals.count()
    approved_goals = goals.filter(status='approved').count()
    completed_goals = 0
    total_achievement = 0
    latest_goals = []

    for goal in goals:

        latest_update = GoalUpdate.objects.filter(
            goal=goal
        ).order_by('-updated_at').first()

        achievement = 0

        if latest_update:
            achievement = latest_update.achievement_value
            total_achievement += achievement
            if achievement >= goal.target:
                completed_goals += 1

        latest_goals.append(
            f"{goal.title} (Target: {goal.target}, Achievement: {achievement})"
        )

    average_achievement = 0
    if total_goals > 0:
        average_achievement = total_achievement / total_goals


    prompt = f"""
Employee: {employee.username}
Goals: {latest_goals}
Approved: {approved_goals}, Completed: {completed_goals}
Avg Achievement: {round(average_achievement, 2)}%

In under 120 words give:
1. Performance Summary
2. Strengths
3. Weaknesses
4. Coaching Suggestions
"""

    ai_response = generate_ai_insights(prompt)

    return {
        "total_goals": total_goals,
        "approved_goals": approved_goals,
        "completed_goals": completed_goals,
        "average_achievement": round(average_achievement, 2),
        "ai_response": ai_response
    }


def generate_ai_copilot_response(employee, question):

    goals = Goal.objects.filter(employee=employee)[:3]

    goal_summary = [
        f"{goal.title} (Status: {goal.status})"
        for goal in goals
    ]


    prompt = f"""
Employee: {employee.username}
Goals: {goal_summary}
Question: {question}

Answer professionally in under 100 words.
"""

    return generate_ai_insights(prompt)


def generate_executive_ai_summary():

    goals = Goal.objects.all()
    updates = GoalUpdate.objects.all()

    total_employees = Goal.objects.values('employee').distinct().count()
    total_goals = goals.count()
    approved_goals = goals.filter(status='approved').count()

    total_achievement = updates.aggregate(
        Avg('achievement_value')
    )['achievement_value__avg'] or 0

    employee_scores = {}
    for update in updates:
        emp = update.goal.employee.username
        employee_scores[emp] = employee_scores.get(emp, 0) + update.achievement_value

    sorted_employees = sorted(
        employee_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_performers = sorted_employees[:5]
    risk_employees = [emp for emp, score in sorted_employees if score < 50]

    prompt = f"""
Organization stats:
- Employees: {total_employees}
- Goals: {total_goals}, Approved: {approved_goals}
- Avg Achievement: {round(total_achievement, 2)}
- Top Performers: {top_performers}
- At Risk: {risk_employees}

In under 150 words give:
• Organization Summary
• Productivity Analysis
• Risk Analysis
• HR Recommendations
"""

    ai_summary = generate_ai_insights(prompt)

    return {
        "total_employees": total_employees,
        "total_goals": total_goals,
        "approved_goals": approved_goals,
        "average_achievement": round(total_achievement, 2),
        "top_performers": top_performers,
        "risk_employees": risk_employees,
        "ai_summary": ai_summary
    }