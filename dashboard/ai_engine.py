import google.generativeai as genai

from django.conf import settings

from goals.models import Goal, GoalUpdate


genai.configure(
    api_key="AIzaSyDlar1FFJyzl7nXpjD0XXO1jRDHWJaM8TU"
)

model = genai.GenerativeModel(
    'models/text-bison-001'
)

def generate_ai_insights(prompt):

    try:

        response = model.generate_text(
            prompt=prompt
        )

        return response.text

    except Exception as e:

        return f"AI Error: {str(e)}"

def generate_employee_insight(employee):

    goals = Goal.objects.filter(
        employee=employee
    )

    total_goals = goals.count()

    approved_goals = goals.filter(
        status='approved'
    ).count()

    completed_goals = 0

    total_achievement = 0

    goal_summary = ""

    update_summary = ""

    for goal in goals:

        goal_summary += f"""

        Goal Title: {goal.title}

        Description: {goal.description}

        Target: {goal.target}

        Weightage: {goal.weightage}

        Status: {goal.status}

        """

        latest_update = GoalUpdate.objects.filter(
            goal=goal
        ).order_by('-updated_at').first()

        if latest_update:

            achievement = latest_update.achievement_value

            total_achievement += achievement

            update_summary += f"""

            Quarter: {latest_update.quarter}

            Achievement Value:
            {latest_update.achievement_value}

            Employee Comment:
            {latest_update.employee_comment}

            """

            if achievement >= goal.target:

                completed_goals += 1


    average_achievement = 0

    if total_goals > 0:

        average_achievement = (
            total_achievement / total_goals
        )

    prompt = f"""

    You are an enterprise AI HR assistant.

    Analyze this employee professionally.

    EMPLOYEE:
    {employee.username}

    TOTAL GOALS:
    {total_goals}

    APPROVED GOALS:
    {approved_goals}

    COMPLETED GOALS:
    {completed_goals}

    AVERAGE ACHIEVEMENT:
    {round(average_achievement, 2)}%

    GOAL DETAILS:
    {goal_summary}

    QUARTERLY UPDATES:
    {update_summary}

    Generate:

    1. Performance Summary

    2. Productivity Analysis

    3. Goal Achievement Review

    4. Strengths

    5. Weaknesses

    6. Performance Risk Level

    7. Coaching Suggestions

    8. Manager Recommendations

    9. Growth Potential

    Keep response professional.
    """

    ai_response = generate_ai_insights(
        prompt
    )

    return {

        "total_goals": total_goals,

        "approved_goals": approved_goals,

        "completed_goals": completed_goals,

        "average_achievement": round(
            average_achievement,
            2
        ),

        "ai_response": ai_response

    }