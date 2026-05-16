from django.shortcuts import render, redirect

from django.contrib.auth import (
    authenticate,
    login,
    logout
)


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