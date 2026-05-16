from django.http import HttpResponse
from reportlab.pdfgen import canvas

from goals.models import Goal
from dashboard.ai_engine import generate_employee_insight


def export_employee_report(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="employee_report.pdf"'

    pdf = canvas.Canvas(response)

    # TITLE

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        200,
        800,
        "Employee Performance Report"
    )

    # EMPLOYEE DETAILS

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        760,
        f"Employee: {request.user.username}"
    )

    # GOALS

    goals = Goal.objects.filter(
        employee=request.user
    )

    y = 720

    pdf.drawString(
        50,
        y,
        "Goals Summary:"
    )

    y -= 30

    for goal in goals:

        pdf.drawString(
            70,
            y,
            f"{goal.title} | Status: {goal.status}"
        )

        y -= 25

    # AI INSIGHTS

    insight = generate_employee_insight(
        request.user
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        "AI Performance Insight:"
    )

    y -= 30

    text_object = pdf.beginText(
        50,
        y
    )

    text_object.setFont(
        "Helvetica",
        11
    )

    for line in insight.split('\n'):

        text_object.textLine(line)

    pdf.drawText(text_object)

    pdf.showPage()

    pdf.save()

    return response