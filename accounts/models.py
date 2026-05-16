from django.db import models
from django.contrib.auth.models import AbstractUser


# DEPARTMENT MODEL

class Department(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return self.name


# CUSTOM USER MODEL

class User(AbstractUser):

    ROLE_CHOICES = (

        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('hr', 'HR'),

    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    # DEPARTMENT RELATION

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # MANAGER RELATIONSHIP

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    def __str__(self):

        return self.username