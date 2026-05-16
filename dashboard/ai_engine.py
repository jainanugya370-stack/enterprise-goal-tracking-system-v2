from goals.models import Goal, GoalUpdate


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

    for goal in goals:

        latest_update = GoalUpdate.objects.filter(
            goal=goal
        ).order_by('-updated_at').first()

        if latest_update:

            achievement = latest_update.achievement_value

            total_achievement += achievement

            if achievement >= goal.target:
                completed_goals += 1

    average_achievement = 0

    if total_goals > 0:

        average_achievement = (
            total_achievement / total_goals
        )

    # AI Insight Logic

    if average_achievement >= 80:

        performance = "excellent"

    elif average_achievement >= 50:

        performance = "good"

    else:

        performance = "needs improvement"

    insight = f"""

    Employee currently has {total_goals} active goals.

    {approved_goals} goals are approved.

    Overall performance trend is {performance}.

    Completed goals count: {completed_goals}.

    Average achievement score is {round(average_achievement, 2)}%.

    Recommended focus:
    improve consistency and quarterly execution.

    """

    return insight