from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import GoalForm, GoalUpdateForm, ManagerCheckInForm
from .models import Goal, GoalUpdate, ManagerCheckIn
from notifications.utils import create_notification


@login_required
def create_goal(request):

    if Goal.objects.filter(employee=request.user, is_locked=True).exists():
        return render(request, 'dashboard/create_goal.html', {
            'form': GoalForm(),
            'error': 'Goals are locked'
        })

    if request.method == 'POST':

        form = GoalForm(request.POST)

        if form.is_valid():

            employee_goals = Goal.objects.filter(employee=request.user)

            if employee_goals.count() >= 8:
                return render(request, 'dashboard/create_goal.html', {
                    'form': form,
                    'error': 'Maximum 8 goals allowed'
                })

            goal = form.save(commit=False)
            goal.employee = request.user

            if goal.weightage < 10:
                return render(request, 'dashboard/create_goal.html', {
                    'form': form,
                    'error': 'Minimum weightage is 10%'
                })

            goal.save()
            return redirect('employee_goals')

    else:
        form = GoalForm()

    return render(request, 'dashboard/create_goal.html', {'form': form})


@login_required
def employee_goals(request):

    goals = Goal.objects.filter(employee=request.user)
    total_weightage = sum(goal.weightage for goal in goals)

    return render(request, 'dashboard/employee_goals.html', {
        'goals': goals,
        'total_weightage': total_weightage
    })


@login_required
def submit_goals(request):

    goals = Goal.objects.filter(employee=request.user)
    total_weightage = sum(goal.weightage for goal in goals)

    if total_weightage != 100:
        return render(request, 'dashboard/employee_goals.html', {
            'goals': goals,
            'total_weightage': total_weightage,
            'error': 'Total weightage must equal 100%'
        })

    goals.update(status='submitted')
    return redirect('employee_goals')


@login_required
def manager_goal_reviews(request):

    team_goals = Goal.objects.all()

    return render(request, 'dashboard/manager_goal_reviews.html', {
        'team_goals': team_goals
    })


@login_required
def approve_goal(request, goal_id):

    goal = Goal.objects.get(id=goal_id)
    goal.status    = 'approved'
    goal.is_locked = True
    goal.save()

    create_notification(
        user=goal.employee,
        title='Goal Approved',
        message=f'Your goal "{goal.title}" was approved by manager.'
    )

    return redirect('manager_goal_reviews')


@login_required
def reject_goal(request, goal_id):

    goal = Goal.objects.get(id=goal_id)
    goal.status    = 'rejected'
    goal.is_locked = False
    goal.save()

    create_notification(
        user=goal.employee,
        title='Goal Rejected',
        message=f'Your goal "{goal.title}" was rejected.'
    )

    return redirect('manager_goal_reviews')


@login_required
def add_goal_update(request, goal_id):

    goal = Goal.objects.get(id=goal_id)

    if request.method == 'POST':
        form = GoalUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.goal = goal
            update.save()
            return redirect('employee_goals')
    else:
        form = GoalUpdateForm()

    return render(request, 'dashboard/add_goal_update.html', {
        'form': form,
        'goal': goal
    })


@login_required
def goal_update_history(request, goal_id):

    goal    = Goal.objects.get(id=goal_id)
    updates = GoalUpdate.objects.filter(goal=goal)

    return render(request, 'dashboard/goal_update_history.html', {
        'goal':    goal,
        'updates': updates
    })


@login_required
def manager_checkin(request, goal_id):

    goal = Goal.objects.get(id=goal_id)

    if request.method == 'POST':
        form = ManagerCheckInForm(request.POST)
        if form.is_valid():
            checkin         = form.save(commit=False)
            checkin.goal    = goal
            checkin.manager = request.user
            checkin.save()

            create_notification(
                user=goal.employee,
                title='Manager Feedback Added',
                message='Your manager added a performance check-in.'
            )

            return redirect('manager_goal_reviews')
    else:
        form = ManagerCheckInForm()

    return render(request, 'dashboard/manager_checkin.html', {
        'form': form,
        'goal': goal
    })