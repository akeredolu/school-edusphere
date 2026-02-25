from django.db import models
import uuid
from students.models import StudentProfile
from schools.models import School
from academics.models import AcademicClass

# -------------------
# Fee Categories / Fees
# -------------------
class FeeCategory(models.Model):
    """
    Defines a fee type for a school or class.
    Combines previous FeeCategory and new Fee models.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    classroom = models.ForeignKey(AcademicClass, on_delete=models.CASCADE, null=True, blank=True)
    term = models.CharField(max_length=50, null=True, blank=True)  # Optional term-specific fee

    def __str__(self):
        return f"{self.name} - {self.amount}"


# -------------------
# Invoices
# -------------------
class Invoice(models.Model):
    """
    Represents a student's invoice for a specific fee.
    Combines previous Invoice fields and new structure.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    fee = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, unique=True)
    term = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("paid", "Paid")],
        default="pending"
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.fee.name} - {self.term}"


# -------------------
# Payments
# -------------------
class Payment(models.Model):
    """
    Represents a payment made against an invoice.
    Combines previous Payment models with verification and method.
    """
    PAYMENT_METHODS = (
        ('paystack', 'Paystack'),
        ('bank', 'Bank Transfer'),
    )

    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice.student.user.email} - {self.amount} ({self.method})"
