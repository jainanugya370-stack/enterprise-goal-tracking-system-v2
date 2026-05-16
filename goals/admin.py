from django.contrib import admin
from .models import Goal, GoalUpdate, ManagerCheckIn

admin.site.register(Goal)
admin.site.register(GoalUpdate)
admin.site.register(ManagerCheckIn)