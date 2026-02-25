from rest_framework import serializers
from .models import FeeCategory, Invoice, Payment

# -------------------
# FeeCategory Serializer
# -------------------
class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = '__all__'


# -------------------
# Invoice Serializer
# -------------------
class InvoiceSerializer(serializers.ModelSerializer):
    # Include fee details for convenience
    fee_name = serializers.CharField(source="fee.name", read_only=True)
    fee_amount = serializers.DecimalField(source="fee.amount", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


# -------------------
# Payment Serializer
# -------------------
class PaymentSerializer(serializers.ModelSerializer):
    # Include related fee name via invoice
    invoice_fee_name = serializers.CharField(source="invoice.fee.name", read_only=True)
    invoice_student_email = serializers.CharField(source="invoice.student.user.email", read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
