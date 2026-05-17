from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from goals.models import Goal
from goals.utils import (
    calculate_employee_performance,
    get_performance_rating,
    calculate_goal_completion
)
from accounts.models import User
from .ai_engine import generate_employee_insight
from accounts.models import Department
from django.shortcuts import render
from goals.models import Goal, GoalUpdate
from dashboard.ai_engine import generate_ai_insights
from dashboard.utils.prompt_builder import build_employee_analysis_prompt
from dashboard.ai_engine import (
    generate_ai_copilot_response
)
from dashboard.ai_engine import (
    generate_executive_ai_summary
)
from django.http import JsonResponse

def ai_copilot_ajax(request):

    if request.method == "POST":

        question = request.POST.get(
            "question"
        )

        response = generate_ai_copilot_response(
            request.user,
            question
        )

        return JsonResponse({

            "response": response

        })

    return JsonResponse({

        "response": "Invalid request"

    })


def executive_dashboard(request):

    executive_data = (
        generate_executive_ai_summary()
    )

    return render(

        request,

        "dashboard/executive_dashboard.html",

        executive_data

    )

def ai_employee_insights(request):

    employee = request.user

    # Fetch employee goals
    goals = Goal.objects.filter(
        employee=employee
    )

    # Fetch employee quarterly updates
    updates = GoalUpdate.objects.filter(
        goal__employee=employee
    )

    # Build goal text for AI
    goal_text = ""

    for goal in goals:

        goal_text += f"""
        Goal Title: {goal.title}
        Description: {goal.description}
        Target: {goal.target}
        Weightage: {goal.weightage}
        Status: {goal.status}

        """

    # Build update text for AI
    update_text = ""

    for update in updates:

        update_text += f"""
        Quarter: {update.quarter}
        Achievement Value: {update.achievement_value}
        Employee Comment: {update.employee_comment}

        """

    # Generate AI Prompt
    prompt = build_employee_analysis_prompt(
        employee,
        goal_text,
        update_text
    )

    # Generate AI Result
    ai_result = generate_ai_insights(prompt)

    context = {
        "ai_result": ai_result,
        "goals": goals,
        "updates": updates,
    }

    return render(
        request,
        "dashboard/ai_insights.html",
        context
    )

@login_required
def employee_dashboard(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if request.user.is_staff:
        return redirect('manager_dashboard')

    goals = Goal.objects.filter(employee=request.user)

    total_goals     = goals.count()
    approved_goals  = goals.filter(status='approved').count()
    completed_goals = goals.filter(status='completed').count()

    performance_score = 0
    if total_goals > 0:
        performance_score = round(
            (approved_goals / total_goals) * 100, 2
        )


    context = {
        'total_goals':       total_goals,
        'approved_goals':    approved_goals,
        'completed_goals':   completed_goals,
        'performance_score': performance_score,
    }

    return render(request, 'employee_dashboard.html', context)


@login_required
def employee_analytics(request):

    if request.user.is_staff or request.user.is_superuser:
        return redirect('manager_analytics')

    employee = request.user
    goals    = Goal.objects.filter(employee=employee)

    total_goals     = goals.count()
    completed_goals = 0
    goal_labels     = []
    goal_scores     = []

    for goal in goals:
        completion = calculate_goal_completion(goal)
        goal_labels.append(goal.title)
        goal_scores.append(completion)
        if completion >= 100:
            completed_goals += 1

    performance_score  = calculate_employee_performance(employee)
    performance_rating = get_performance_rating(performance_score)

    completion_percentage = 0
    if total_goals > 0:
        completion_percentage = round(
            (completed_goals / total_goals) * 100, 2
        )

    import json

    context = {
        'goals':                  goals,
        'total_goals':            total_goals,
        'completed_goals':        completed_goals,
        'performance_score':      performance_score,
        'performance_rating':     performance_rating,
        'completion_percentage':  completion_percentage,
        'goal_labels':            json.dumps(goal_labels),
        'goal_scores':            json.dumps(goal_scores),
    }

    return render(request, 'dashboard/employee_analytics.html', context)


@login_required
def manager_dashboard(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if not request.user.is_staff:
        return redirect('employee_dashboard')

    return render(request, 'manager_dashboard.html')


@login_required
def manager_analytics(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('employee_analytics')

    employees = User.objects.filter(role='employee')

    leaderboard = []
    for employee in employees:
        score = calculate_employee_performance(employee)
        leaderboard.append({
            'employee': employee,
            'score':    score,
            'rating':   get_performance_rating(score),
        })

    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)

    context = {
        'leaderboard':    leaderboard,
        'top_performers': leaderboard[:5],
    }

    return render(request, 'dashboard/manager_analytics.html', context)

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        if request.user.is_staff:
            return redirect('manager_dashboard')
        return redirect('employee_dashboard')

    employees = User.objects.filter(
        is_staff=False,
        is_superuser=False
    )

    managers = User.objects.filter(
        is_staff=True,
        is_superuser=False
    )

    total_employees = employees.count()
    total_managers  = managers.count()
    total_goals     = Goal.objects.count()

    approved_goals = Goal.objects.filter(status='approved').count()
    pending_goals  = Goal.objects.filter(status='pending').count()

    organization_scores = []
    leaderboard         = []

    for employee in employees:
        score = calculate_employee_performance(employee)
        organization_scores.append(score)
        leaderboard.append({
            'employee': employee,
            'score':    score,
            'rating':   get_performance_rating(score),
        })

    average_score = 0
    if organization_scores:
        average_score = round(
            sum(organization_scores) / len(organization_scores), 2
        )

    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)

    context = {
        'total_employees': total_employees,
        'total_managers':  total_managers,
        'total_goals':     total_goals,
        'approved_goals':  approved_goals,
        'pending_goals':   pending_goals,
        'average_score':   average_score,
        'leaderboard':     leaderboard,
        'top_performers':  leaderboard[:5],
    }

    return render(request, 'admin_dashboard.html', context)

def department_analytics(request):

    departments = Department.objects.all()

    analytics = []

    for department in departments:

        employees = department.user_set.all()

        employee_count = employees.count()

        analytics.append({

            'department': department,
            'employee_count': employee_count,

        })

    return render(

        request,

        'department_analytics.html',

        {
            'analytics': analytics
        }
    )

def ai_copilot(request):

    response = None

    if request.method == "POST":

        question = request.POST.get(
            "question"
        )

        response = generate_ai_copilot_response(
            request.user,
            question
        )

    context = {
        "response": response
    }

    return render(
        request,
        "dashboard/ai_copilot.html",
        context
    )