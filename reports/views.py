from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas

from goals.models import Goal
from dashboard.ai_engine import generate_employee_insight


@login_required
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
    pdf.drawString(200, 800, "Employee Performance Report")

    # EMPLOYEE DETAILS

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Employee: {request.user.username}")

    # GOALS

    goals = Goal.objects.filter(employee=request.user)

    y = 720

    pdf.drawString(50, y, "Goals Summary:")
    y -= 30

    for goal in goals:
        pdf.drawString(
            70, y,
            f"{goal.title} | Status: {goal.status}"
        )
        y -= 25

        # Start a new page if running out of space
        if y < 100:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 780

    # AI INSIGHTS

    insight_data = generate_employee_insight(request.user)
    insight_text = insight_data.get('ai_response', 'AI insights unavailable.')

    y -= 20

    pdf.drawString(50, y, "AI Performance Insight:")
    y -= 30

    text_object = pdf.beginText(50, y)
    text_object.setFont("Helvetica", 11)

    # Wrap long lines so they don't overflow the page width
    for line in insight_text.split('\n'):

        # Break lines longer than 90 chars into chunks
        while len(line) > 90:
            text_object.textLine(line[:90])
            line = line[90:]

        text_object.textLine(line)

        # Check for page overflow
        if text_object.getY() < 60:
            pdf.drawText(text_object)
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            text_object = pdf.beginText(50, 780)
            text_object.setFont("Helvetica", 11)

    pdf.drawText(text_object)

    pdf.showPage()
    pdf.save()

    return response