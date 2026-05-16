from django.db import models
from accounts.models import User


class Goal(models.Model):

    UOM_CHOICES = (
        ('numeric', 'Numeric'),
        ('percentage', 'Percentage'),
        ('timeline', 'Timeline'),
        ('zero', 'Zero Based'),
    )

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    thrust_area = models.CharField(max_length=100)

    uom_type = models.CharField(
        max_length=20,
        choices=UOM_CHOICES
    )

    target = models.FloatField()

    weightage = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class GoalUpdate(models.Model):

    QUARTER_CHOICES = (

        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),

    )

    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quarter = models.CharField(
        max_length=2,
        choices=QUARTER_CHOICES
    )

    achievement_value = models.FloatField(
        default=0
    )

    employee_comment = models.TextField(
        default=''
    )

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.goal.title} - {self.quarter}"


class ManagerCheckIn(models.Model):

    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    discussion_notes = models.TextField(
        default=''
    )

    manager_feedback = models.TextField(
        default=''
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.goal.title} Check-In"