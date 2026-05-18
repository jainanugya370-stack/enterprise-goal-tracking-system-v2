from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

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

    if request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.user.is_staff or request.user.role == 'manager':
        return redirect('manager_dashboard')

    goals           = Goal.objects.filter(employee=request.user)
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

    total_employees = User.objects.filter(
        role='employee'
    ).count()

    total_managers = User.objects.filter(
        role='manager'
    ).count()

    approved_goals = Goal.objects.filter(
        status='approved'
    ).count()

    total_goals = Goal.objects.count()

    if total_goals > 0:
        avg_performance = int(
            (approved_goals / total_goals) * 100
        )
    else:
        avg_performance = 0

    top_performers = Goal.objects.filter(
        status='approved'
    ).select_related('employee')[:5]

    context = {
        'total_employees': total_employees,
        'total_managers': total_managers,
        'approved_goals': approved_goals,
        'avg_performance': avg_performance,
        'top_performers': top_performers,
    }

    return render(
        request,
        'dashboard/admin_dashboard.html',
        context
    )


# ─────────────────────────────────────────────
# DEPARTMENT ANALYTICS
# ─────────────────────────────────────────────

@login_required
def department_analytics(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('employee_dashboard')

    departments = Department.objects.all()
    analytics   = []

    for dept in departments:
        analytics.append({
            'department':    dept,
            'employee_count': User.objects.filter(department=dept).count(),
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

    prompt    = build_employee_analysis_prompt(employee, goal_text, update_text)
    ai_result = generate_ai_insights(prompt)

    context = {
        'ai_result': ai_result,
        'goals':     goals,
        'updates':   updates,
    }

    return render(request, 'dashboard/ai_insights.html', context)


# ─────────────────────────────────────────────
# AI COPILOT
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


# ─────────────────────────────────────────────
# DEMO DATA SETUP (browser-based, no shell)
# Visit /dashboard/setup-demo-data/ once
# ─────────────────────────────────────────────

def setup_demo_data(request):
    """
    Creates realistic demo data:
    - 3 departments
    - 3 managers
    - 6 employees assigned to departments
    - 2-3 goals per employee
    - goal updates with achievement values
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    log = []

    # ── DEPARTMENTS ──────────────────────────────
    dept_names = ['Engineering', 'Marketing', 'Operations']
    departments = {}

    for name in dept_names:
        dept, created = Department.objects.get_or_create(name=name)
        departments[name] = dept
        if created:
            log.append(f"✅ Department created: {name}")
        else:
            log.append(f"ℹ️  Department exists: {name}")

    # ── MANAGERS ─────────────────────────────────
    managers_data = [
        {'username': 'manager_eng',  'password': 'Manager@1234', 'dept': 'Engineering'},
        {'username': 'manager_mkt',  'password': 'Manager@1234', 'dept': 'Marketing'},
        {'username': 'manager_ops',  'password': 'Manager@1234', 'dept': 'Operations'},
    ]

    managers = {}
    for m in managers_data:
        if not User.objects.filter(username=m['username']).exists():
            user = User.objects.create_user(
                username=m['username'],
                password=m['password'],
                email=f"{m['username']}@goalsync.com",
            )
            user.role       = 'manager'
            user.is_staff   = True
            user.department = departments[m['dept']]
            user.save()
            managers[m['dept']] = user
            log.append(f"✅ Manager created: {m['username']}")
        else:
            managers[m['dept']] = User.objects.get(username=m['username'])
            log.append(f"ℹ️  Manager exists: {m['username']}")

    # ── EMPLOYEES ─────────────────────────────────
    employees_data = [
        {'username': 'alice',   'dept': 'Engineering', 'password': 'Employee@1234'},
        {'username': 'bob',     'dept': 'Engineering', 'password': 'Employee@1234'},
        {'username': 'carol',   'dept': 'Marketing',   'password': 'Employee@1234'},
        {'username': 'david',   'dept': 'Marketing',   'password': 'Employee@1234'},
        {'username': 'eve',     'dept': 'Operations',  'password': 'Employee@1234'},
        {'username': 'frank',   'dept': 'Operations',  'password': 'Employee@1234'},
    ]

    employees = []
    for e in employees_data:
        if not User.objects.filter(username=e['username']).exists():
            user = User.objects.create_user(
                username=e['username'],
                password=e['password'],
                email=f"{e['username']}@goalsync.com",
            )
            user.role       = 'employee'
            user.is_staff   = False
            user.department = departments[e['dept']]
            user.manager    = managers[e['dept']]
            user.save()
            log.append(f"✅ Employee created: {e['username']}")
        else:
            user = User.objects.get(username=e['username'])
            log.append(f"ℹ️  Employee exists: {e['username']}")
        employees.append(user)

    # ── GOALS ─────────────────────────────────────
    goals_data = [
        {'title': 'Complete Q1 Sprint',        'target': 100, 'weightage': 40, 'status': 'approved'},
        {'title': 'Improve Code Review Score', 'target': 90,  'weightage': 30, 'status': 'approved'},
        {'title': 'Complete Training Program', 'target': 80,  'weightage': 30, 'status': 'submitted'},
    ]

    for employee in employees:
        existing = Goal.objects.filter(employee=employee).count()
        if existing == 0:
            for g in goals_data:
                Goal.objects.create(
                    employee=employee,
                    title=g['title'],
                    description=f"Performance goal for {employee.username}",
                    target=g['target'],
                    weightage=g['weightage'],
                    status=g['status'],
                )
            log.append(f"✅ Goals created for: {employee.username}")

            # ── GOAL UPDATES ──────────────────────
            approved_goals = Goal.objects.filter(
                employee=employee, status='approved'
            )
            achievements = [75, 85, 90, 60, 95, 70]
            for i, goal in enumerate(approved_goals):
                GoalUpdate.objects.create(
                    goal=goal,
                    quarter='Q1',
                    achievement_value=achievements[i % len(achievements)],
                    employee_comment='Making steady progress on this goal.',
                )
            log.append(f"✅ Updates created for: {employee.username}")
        else:
            log.append(f"ℹ️  Goals exist for: {employee.username} ({existing} goals)")

    # ── SUMMARY ───────────────────────────────────
    html = "<h2>GoalSync Demo Data Setup</h2><pre>"
    html += "\n".join(log)
    html += f"""

─────────────────────────────
📊 Summary:
   Departments : {Department.objects.count()}
   Managers    : {User.objects.filter(role='manager').count()}
   Employees   : {User.objects.filter(role='employee').count()}
   Goals       : {Goal.objects.count()}
   Updates     : {GoalUpdate.objects.count()}

📋 Employee Logins (password: Employee@1234):
   alice / bob / carol / david / eve / frank

📋 Manager Logins (password: Manager@1234):
   manager_eng / manager_mkt / manager_ops

✅ Done! Go to /login/ to test.
</pre>
<a href="/login/">→ Go to Login</a> &nbsp;|&nbsp;
<a href="/list-users/">→ List All Users</a>"""

    return HttpResponse(html)