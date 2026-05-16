from django import forms
from .models import Goal
from .models import GoalUpdate, ManagerCheckIn

class GoalForm(forms.ModelForm):

    class Meta:

        model = Goal

        fields = [
            'title',
            'description',
            'thrust_area',
            'uom_type',
            'target',
            'weightage',
        ]

        widgets = {

            'description': forms.Textarea(
                attrs={'rows': 3}
            ),

        }

class GoalUpdateForm(forms.ModelForm):

    class Meta:

        model = GoalUpdate

        fields = [
            'quarter',
            'achievement_value',
            'employee_comment',
        ]


class ManagerCheckInForm(forms.ModelForm):

    class Meta:

        model = ManagerCheckIn

        fields = [
            'discussion_notes',
            'manager_feedback',
        ]