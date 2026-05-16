from .models import Goal, GoalUpdate


def calculate_goal_completion(goal):
    """
    Returns latest achievement percentage for a goal.
    """

    latest_update = GoalUpdate.objects.filter(
        goal=goal
    ).order_by('-updated_at').first()

    if latest_update:
        return latest_update.achievement_value

    return 0


def calculate_employee_performance(employee):

    goals = Goal.objects.filter(employee=employee)

    total_score = 0
    total_weightage = 0

    for goal in goals:

        completion = calculate_goal_completion(goal)

        weighted_score = (
            completion * goal.weightage
        ) / 100

        total_score += weighted_score
        total_weightage += goal.weightage

    if total_weightage == 0:
        return 0

    return round(total_score, 2)


def get_performance_rating(score):

    if score >= 90:
        return "Outstanding"

    elif score >= 75:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    return "Needs Improvement"