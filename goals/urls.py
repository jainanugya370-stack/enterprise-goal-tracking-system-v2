from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/',
        views.create_goal,
        name='create_goal'
    ),

    path(
        'my-goals/',
        views.employee_goals,
        name='employee_goals'
    ),

    path(
        'submit/',
        views.submit_goals,
        name='submit_goals'
    ),

    path(
        'manager-reviews/',
        views.manager_goal_reviews,
        name='manager_goal_reviews'
    ),

    path(
        'approve/<int:goal_id>/',
        views.approve_goal,
        name='approve_goal'
    ),

    path(
        'reject/<int:goal_id>/',
        views.reject_goal,
        name='reject_goal'
    ),

    path(
        'add-update/<int:goal_id>/',
        views.add_goal_update,
        name='add_goal_update'
    ),

    path(
        'history/<int:goal_id>/',
        views.goal_update_history,
        name='goal_update_history'
    ),

    path(
        'manager-checkin/<int:goal_id>/',
        views.manager_checkin,
        name='manager_checkin'
    ),

]