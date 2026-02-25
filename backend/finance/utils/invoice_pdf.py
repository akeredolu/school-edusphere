from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_invoice_pdf(invoice, file_path):
    c = canvas.Canvas(file_path, pagesize=A4)

    c.drawString(50, 800, "SCHOOL NAME")
    c.drawString(50, 770, f"Student: {invoice.student}")
    c.drawString(50, 740, f"Term: {invoice.term}")
    c.drawString(50, 710, f"Total: ₦{invoice.total_amount}")
    c.drawString(50, 680, f"Paid: ₦{invoice.amount_paid}")

    c.save()

