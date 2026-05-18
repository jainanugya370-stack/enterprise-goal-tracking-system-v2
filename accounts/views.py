from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


def login_view(request):

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
    if user.is_superuser:
        return redirect("/dashboard/admin/")
    if user.is_staff or user.role == "manager":
        return redirect("/dashboard/manager/")
    return redirect("/dashboard/employee/")


def logout_view(request):
    logout(request)
    return redirect("/login/")

def setup_users(request):
    """
    Visit /setup-users/ to create all demo users at once.
    """
    users_to_create = [
        {
            'username':     'hr_admin',
            'password':     'Admin@1234',
            'email':        'admin@goalsync.com',
            'role':         'hr',
            'is_superuser': True,
            'is_staff':     True,
        },
        {
            'username':     'manager1',
            'password':     'Manager@1234',
            'email':        'manager@goalsync.com',
            'role':         'manager',
            'is_superuser': False,
            'is_staff':     True,
        },
        {
            'username':     'employee1',
            'password':     'Employee@1234',
            'email':        'employee1@goalsync.com',
            'role':         'employee',
            'is_superuser': False,
            'is_staff':     False,
        },
        {
            'username':     'employee2',
            'password':     'Employee@1234',
            'email':        'employee2@goalsync.com',
            'role':         'employee',
            'is_superuser': False,
            'is_staff':     False,
        },
    ]

    created = []
    skipped = []

    for u in users_to_create:
        if User.objects.filter(username=u['username']).exists():
            skipped.append(u['username'])
            continue

        user = User.objects.create_user(
            username=u['username'],
            password=u['password'],
            email=u['email'],
        )
        user.role         = u['role']
        user.is_superuser = u['is_superuser']
        user.is_staff     = u['is_staff']
        user.save()
        created.append(u['username'])

    html = "<h2>GoalSync User Setup</h2><pre>"

    if created:
        html += "✅ Created:\n"
        for u in created:
            html += f"   {u}\n"

    if skipped:
        html += "\nℹ️ Already existed (skipped):\n"
        for u in skipped:
            html += f"   {u}\n"

    html += """
📋 Credentials:
   hr_admin   /  Admin@1234    →  Admin Dashboard
   manager1   /  Manager@1234  →  Manager Dashboard
   employee1  /  Employee@1234 →  Employee Dashboard
   employee2  /  Employee@1234 →  Employee Dashboard

✅ Done. Go to /login/
</pre><a href="/login/">→ Go to Login</a>"""

    return HttpResponse(html)


def reset_password(request, username, new_password):
    """
    Visit /reset-password/username/newpassword/ to reset a user's password.
    Example: /reset-password/manager1/NewPass@123/
    """
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return HttpResponse(
            f"<pre>✅ Password for '{username}' updated to '{new_password}'</pre>"
            f"<a href='/login/'>→ Go to Login</a>"
        )
    except User.DoesNotExist:
        return HttpResponse(
            f"<pre>❌ User '{username}' not found.\n"
            f"Visit /setup-users/ first to create users.</pre>"
        )


def list_users(request):
    """
    Visit /list-users/ to see all users and their roles.
    """
    users = User.objects.all().values(
        'username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active'
    )

    html = "<h2>GoalSync — All Users</h2><pre>"
    html += f"{'Username':<20} {'Role':<12} {'Staff':<8} {'Superuser':<12} Active\n"
    html += "-" * 65 + "\n"

    for u in users:
        html += (
            f"{u['username']:<20} {u['role']:<12} "
            f"{str(u['is_staff']):<8} {str(u['is_superuser']):<12} "
            f"{u['is_active']}\n"
        )

    html += "</pre>"
    return HttpResponse(html)