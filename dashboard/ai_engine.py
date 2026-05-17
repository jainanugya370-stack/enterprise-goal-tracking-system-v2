# import google.generativeai as genai
#
# from django.conf import settings
#
# from goals.models import Goal, GoalUpdate
#
#
# genai.configure(
#     api_key="AIzaSyDlar1FFJyzl7nXpjD0XXO1jRDHWJaM8TU"
# )
#
# model = genai.GenerativeModel(
#     'models/text-bison-001'
# )
#
# def generate_ai_insights(prompt):
#
#     try:
#
#         response = model.generate_content(
#             prompt
#         )
#
#         return response.text
#
#     except Exception as e:
#
#         return f"AI Error: {str(e)}"

import google.generativeai as genai
from goals.models import Goal, GoalUpdate

genai.configure(api_key="...")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_ai_insights(prompt):
    response = model.generate_content(prompt)
    return response.text


from google import genai
client = genai.Client(api_key="AIzaSyAi81KmViPV153-XSanGpz2GizxTzjf_QU")

def generate_ai_insights(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        error = str(e)
        if '429' in error or 'RESOURCE_EXHAUSTED' in error:
            return "AI insights are temporarily unavailable due to API quota limits. Please try again later."
        elif '404' in error:
            return "AI model is currently unavailable. Please try again later."
        else:
            return "AI insights are currently unavailable. Please try again later."

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

# AI Copilot
def generate_ai_copilot_response(employee, question):

    goals = Goal.objects.filter(
        employee=employee
    )

    updates = GoalUpdate.objects.filter(
        goal__employee=employee
    )

    goal_summary = ""

    update_summary = ""

#goal data
    for goal in goals:

        goal_summary += f"""

        Goal:
        {goal.title}

        Description:
        {goal.description}

        Target:
        {goal.target}

        Status:
        {goal.status}

        """

# update
    for update in updates:

        update_summary += f"""

        Quarter:
        {update.quarter}

        Achievement:
        {update.achievement_value}

        Comment:
        {update.employee_comment}

        """

# AI prompt
    prompt = f"""

    You are an enterprise HR AI Copilot.

    Employee:
    {employee.username}

    Employee Goals:
    {goal_summary}

    Quarterly Updates:
    {update_summary}

    USER QUESTION:
    {question}

    Respond professionally and clearly.
    """

    return generate_ai_insights(prompt)

from django.db.models import Avg


def generate_executive_ai_summary():

    goals = Goal.objects.all()

    updates = GoalUpdate.objects.all()

    total_employees = Goal.objects.values(
        'employee'
    ).distinct().count()

    total_goals = goals.count()

    approved_goals = goals.filter(
        status='approved'
    ).count()

    total_achievement = updates.aggregate(
        Avg('achievement_value')
    )['achievement_value__avg']

    if not total_achievement:
        total_achievement = 0

    top_performers = []

    employee_scores = {}

    for update in updates:

        employee = update.goal.employee.username

        if employee not in employee_scores:

            employee_scores[employee] = 0

        employee_scores[employee] += (
            update.achievement_value
        )

    sorted_employees = sorted(
        employee_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_performers = sorted_employees[:5]

    risk_employees = []

    for employee, score in sorted_employees:

        if score < 50:

            risk_employees.append(employee)

    prompt = f"""

    You are an enterprise HR AI strategist.

    Analyze this organization.

    TOTAL EMPLOYEES:
    {total_employees}

    TOTAL GOALS:
    {total_goals}

    APPROVED GOALS:
    {approved_goals}

    AVERAGE ACHIEVEMENT:
    {round(total_achievement, 2)}

    TOP PERFORMERS:
    {top_performers}

    RISK EMPLOYEES:
    {risk_employees}

    Generate:

    1. Organization Performance Summary

    2. Productivity Analysis

    3. Workforce Risk Analysis

    4. Department Improvement Suggestions

    5. HR Strategic Recommendations

    6. Growth Opportunities

    Keep it executive-level and professional.
    """

    ai_summary = generate_ai_insights(
        prompt
    )

    return {

        "total_employees":
            total_employees,

        "total_goals":
            total_goals,

        "approved_goals":
            approved_goals,

        "average_achievement":
            round(total_achievement, 2),

        "top_performers":
            top_performers,

        "risk_employees":
            risk_employees,

        "ai_summary":
            ai_summary

    }