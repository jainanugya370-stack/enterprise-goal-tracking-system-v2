from django.urls import path
from . import views

urlpatterns = [

    path('',        views.login_view,  name='login'),
    path('login/',  views.login_view,  name='login_page'),
    path('logout/', views.logout_view, name='logout'),

    path('setup-users/',
         views.setup_users,
         name='setup_users'),

    path('list-users/',
         views.list_users,
         name='list_users'),


    path('reset-password/<str:username>/<str:new_password>/',
         views.reset_password,
         name='reset_password'),

    path(
        'setup-demo-data/',
        views.setup_demo_data,
        name='setup_demo_data'
    ),
]