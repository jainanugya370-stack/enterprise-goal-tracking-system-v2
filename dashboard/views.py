from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from goals.models import Goal, GoalUpdate
from goals.utils import (
    calculate_employee_performance,
    get_performance_rating,
    calculate_goal_completion
)

from accounts.models import User, Department

from dashboard.ai_engine import (
    generate_ai_insights,
    generate_ai_copilot_response,
    generate_executive_ai_summary,
    generate_employee_insight,
)

from dashboard.utils.prompt_builder import build_employee_analysis_prompt

import json


# ─────────────────────────────────────────────
# EMPLOYEE DASHBOARD
# ─────────────────────────────────────────────

@login_required
def employee_dashboard(request):

    # ✅ FIX: Guard superusers and staff away from employee dashboard
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.user.is_staff or request.user.role == 'manager':
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
        'goals':             goals,
        'total_goals':       total_goals,
        'approved_goals':    approved_goals,
        'completed_goals':   completed_goals,
        'performance_score': performance_score,
    }

    return render(request, 'dashboard/employee_dashboard.html', context)


# ─────────────────────────────────────────────
# EMPLOYEE ANALYTICS
# ─────────────────────────────────────────────

@login_required
def employee_analytics(request):

    if request.user.is_staff or request.user.is_superuser:
        return redirect('manager_analytics')

    employee    = request.user
    goals       = Goal.objects.filter(employee=employee)
    total_goals = goals.count()

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

    context = {
        'goals':                 goals,
        'total_goals':           total_goals,
        'completed_goals':       completed_goals,
        'performance_score':     performance_score,
        'performance_rating':    performance_rating,
        'completion_percentage': completion_percentage,
        'goal_labels':           json.dumps(goal_labels),
        'goal_scores':           json.dumps(goal_scores),
    }

    return render(request, 'dashboard/employee_analytics.html', context)


# ─────────────────────────────────────────────
# MANAGER DASHBOARD
# ─────────────────────────────────────────────

@login_required
def manager_dashboard(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')

    if not request.user.is_staff and request.user.role != 'manager':
        return redirect('employee_dashboard')

    return render(request, 'dashboard/manager_dashboard.html')


# ─────────────────────────────────────────────
# MANAGER ANALYTICS
# ─────────────────────────────────────────────

@login_required
def manager_analytics(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('employee_analytics')

    # ✅ Safe: returns empty list if no employees yet
    employees   = User.objects.filter(role='employee')
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


# ─────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        if request.user.is_staff or request.user.role == 'manager':
            return redirect('manager_dashboard')
        return redirect('employee_dashboard')

    employees = User.objects.filter(is_staff=False, is_superuser=False)
    managers  = User.objects.filter(is_staff=True,  is_superuser=False)

    total_employees = employees.count()
    total_managers  = managers.count()
    total_goals     = Goal.objects.count()
    approved_goals  = Goal.objects.filter(status='approved').count()
    pending_goals   = Goal.objects.filter(status='pending').count()

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

    return render(request, 'dashboard/admin_dashboard.html', context)


# ─────────────────────────────────────────────
# DEPARTMENT ANALYTICS
# ─────────────────────────────────────────────

@login_required
def department_analytics(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('employee_dashboard')

    departments = Department.objects.all()
    analytics   = []

    for department in departments:
        analytics.append({
            'department':    department,
            'employee_count': User.objects.filter(department=department).count(),
        })

    return render(
        request,
        'dashboard/department_analytics.html',
        {'analytics': analytics}
    )


# ─────────────────────────────────────────────
# AI EMPLOYEE INSIGHTS
# ─────────────────────────────────────────────

@login_required
def ai_employee_insights(request):

    employee = request.user
    goals    = Goal.objects.filter(employee=employee)
    updates  = GoalUpdate.objects.filter(goal__employee=employee)

    goal_text   = ""
    update_text = ""

    for goal in goals:
        goal_text += (
            f"Goal: {goal.title} | "
            f"Target: {goal.target} | "
            f"Status: {goal.status}\n"
        )

    for update in updates:
        update_text += (
            f"Quarter: {update.quarter} | "
            f"Achievement: {update.achievement_value} | "
            f"Comment: {update.employee_comment}\n"
        )

    prompt   = build_employee_analysis_prompt(employee, goal_text, update_text)
    ai_result = generate_ai_insights(prompt)

    context = {
        'ai_result': ai_result,
        'goals':     goals,
        'updates':   updates,
    }

    return render(request, 'dashboard/ai_insights.html', context)


# ─────────────────────────────────────────────
# AI COPILOT PAGE
# ─────────────────────────────────────────────

@login_required
def ai_copilot(request):

    response = None

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            response = generate_ai_copilot_response(request.user, question)

    return render(
        request,
        'dashboard/ai_copilot.html',
        {'response': response}
    )


# ─────────────────────────────────────────────
# AI COPILOT AJAX
# ─────────────────────────────────────────────

@login_required
def ai_copilot_ajax(request):

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            response = generate_ai_copilot_response(request.user, question)
            return JsonResponse({"response": response})

    return JsonResponse({"response": "Invalid request."})


# ─────────────────────────────────────────────
# EXECUTIVE DASHBOARD
# ─────────────────────────────────────────────

@login_required
def executive_dashboard(request):

    executive_data = generate_executive_ai_summary()
    return render(request, 'dashboard/executive_dashboard.html', executive_data)