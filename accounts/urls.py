from django.urls import path
from . import views

urlpatterns = [

    path('',        views.login_view,  name='login'),
    path('login/',  views.login_view,  name='login_page'),
    path('logout/', views.logout_view, name='logout'),

    # ── Browser-based user management (no shell needed) ──────────────
    # Step 1: Visit this to create all users at once
    path('setup-users/',
         views.setup_users,
         name='setup_users'),

    # Step 2: Visit this to check what users exist and their roles
    path('list-users/',
         views.list_users,
         name='list_users'),

    # Step 3: If a user can't login, reset their password via URL
    # Example: /reset-password/manager1/NewPass@123/
    path('reset-password/<str:username>/<str:new_password>/',
         views.reset_password,
         name='reset_password'),
]