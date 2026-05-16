from django.urls import path
from . import views

urlpatterns = [

    path(
        'employee-pdf/',
        views.export_employee_report,
        name='employee_pdf'
    ),

]