from django.urls import path
from . import views

urlpatterns = [

    path('employee/',          views.employee_dashboard,  name='employee_dashboard'),
    path('manager/',           views.manager_dashboard,   name='manager_dashboard'),
    path('admin/',             views.admin_dashboard,     name='admin_dashboard'),
    path('employee-analytics/', views.employee_analytics, name='employee_analytics'),
    path('manager-analytics/', views.manager_analytics,   name='manager_analytics'),
    path('departments/',       views.department_analytics, name='department_analytics'),
    path('ai-insights/',       views.ai_employee_insights, name='ai_insights'),
    path('ai-copilot/',        views.ai_copilot,           name='ai_copilot'),
    path('ai-copilot-ajax/',   views.ai_copilot_ajax,      name='ai_copilot_ajax'),
    path('executive-dashboard/', views.executive_dashboard, name='executive_dashboard'),

    # One-time setup — visit once on Render then leave it
    path('setup-demo-data/',   views.setup_demo_data,     name='setup_demo_data'),
]