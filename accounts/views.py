from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ROLE-BASED REDIRECTS

            if user.is_superuser:
                return redirect("/dashboard/admin/")

            elif user.role == "manager":
                return redirect("/dashboard/manager/")

            elif user.role == "employee":
                return redirect("/dashboard/employee/")

            else:
                return redirect("/")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "accounts/login.html")


def logout_view(request):

    logout(request)

    return redirect('login')
