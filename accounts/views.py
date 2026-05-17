from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


def login_view(request):

    # Already logged in — redirect to right dashboard
    if request.user.is_authenticated:
        return _role_redirect(request.user)

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return _role_redirect(user)

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")


def _role_redirect(user):
    """
    Central redirect logic — checks is_superuser and is_staff flags FIRST
    (reliable), then falls back to role field.
    Prevents redirect loops when role field is out of sync with flags.
    """
    if user.is_superuser:
        return redirect("/dashboard/admin/")

    # ✅ FIX: Check is_staff OR role == manager — covers users created via
    # Django admin (is_staff=True but role may still be 'employee')
    if user.is_staff or user.role == "manager":
        return redirect("/dashboard/manager/")

    return redirect("/dashboard/employee/")


def logout_view(request):
    logout(request)
    return redirect("/login/")


def create_demo_user(request):
    """
    One-time helper to create a superuser on Render when DB is empty.
    Remove or restrict this after first use.
    """
    if not User.objects.filter(username="hr_admin").exists():
        User.objects.create_superuser(
            username="hr_admin",
            email="hr@goalsync.com",
            password="admin123"
        )
        return HttpResponse("✅ hr_admin superuser created. Login at /login/")

    return HttpResponse("ℹ️ hr_admin already exists.")