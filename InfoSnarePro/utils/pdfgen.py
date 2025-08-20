from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf(data, risk_score, risk_level):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 750, "InfoSnare Pro - Simulated Stolen Data Report")
    c.setFont("Helvetica", 12)
    y = 720
    c.drawString(72, y, f"Risk Score: {risk_score}% ({risk_level})")
    y -= 30
    for k, v in data.items():
        if k in ('timestamp', 'ip_address', 'user_agent', 'session_id'):
            continue
        c.drawString(72, y, f"{k.replace('_', ' ').title()}: {v if v else 'Not provided'}")
        y -= 20
        if y < 100:
            c.showPage()
            y = 750
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(72, 60, f"Timestamp: {data.get('timestamp', '')}")
    c.drawString(72, 45, f"IP: {data.get('ip_address', '')}")
    c.drawString(72, 30, f"Browser: {data.get('user_agent', '')}")
    c.save()
    buffer.seek(0)
    return buffer 