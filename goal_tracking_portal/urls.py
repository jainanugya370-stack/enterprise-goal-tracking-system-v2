from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'dashboard/',
        include('dashboard.urls')
    ),

    path(
        'goals/',
        include('goals.urls')
    ),

    path(
        'notifications/',
        include('notifications.urls')
    ),

    path(
        'reports/',
        include('reports.urls')
    ),
]