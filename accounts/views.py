from django.shortcuts import render, redirect

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


def create_demo_user(request):

    if not User.objects.filter(username="admin").exists():

        User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin123"
        )

    return HttpResponse("Demo superuser created.")

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # HR / ADMIN

            if (
                user.role == 'hr'
                or user.is_superuser
            ):

                return redirect(
                    'admin_dashboard'
                )

            # MANAGER

            elif user.role == 'manager':

                return redirect(
                    'manager_dashboard'
                )

            # EMPLOYEE

            else:

                return redirect(
                    'employee_dashboard'
                )

    return render(
        request,
        'login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')

