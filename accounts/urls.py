from django.urls import path
from .views import login_view, logout_view, create_demo_user

urlpatterns = [

    # HOME LOGIN
    path(
        '',
        login_view,
        name='login'
    ),

    # EXPLICIT LOGIN URL
    path(
        'login/',
        login_view,
        name='login_page'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'create-demo-user/',
        create_demo_user,
        name='create_demo_user'
    ),
]