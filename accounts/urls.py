from django.urls import path
from .views import login_view, logout_view, create_demo_user

urlpatterns = [

    path('', login_view, name='login'),

    path('logout/', logout_view, name='logout'),

    path('create-demo-user/', create_demo_user),

]