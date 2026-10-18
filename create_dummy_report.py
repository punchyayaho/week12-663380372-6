# email-sms-automator/create_dummy_report.py
"""Helper script: creates data/dummy_report.pdf (sample attachment)."""
import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "dummy_report.pdf")
os.makedirs(os.path.dirname(path), exist_ok=True)
c = canvas.Canvas(path, pagesize=A4)
c.setFont("Helvetica-Bold", 20)
c.drawString(72, 770, "Daily Report (Dummy)")
c.setFont("Helvetica", 12)
c.drawString(72, 740, f"Generated: {datetime.date.today().isoformat()}")
c.drawString(72, 720, "This PDF is a sample attachment for the Email & SMS automation lab.")
c.save()
print("Created", path)
