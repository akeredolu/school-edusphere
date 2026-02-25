from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSchoolAdmin
from .models import FeeCategory, Payment
from .serializers import FeeCategorySerializer, PaymentSerializer
from .models import Payment
from .services.paystack import verify_paystack_payment

# ---------------------------
# Fee Category ViewSet
# ---------------------------
class FeeCategoryViewSet(ModelViewSet):
    serializer_class = FeeCategorySerializer
    permission_classes = [IsSchoolAdmin]

    def get_queryset(self):
        # School admins see only their school's fee categories
        return FeeCategory.objects.filter(school=self.request.user.school)


# ---------------------------
# Payment ViewSet
# ---------------------------
class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Students see only their own payments
        if hasattr(user, 'studentprofile'):
            return Payment.objects.filter(student=user.studentprofile)
        # Admins could extend logic here if needed
        return Payment.objects.none()


# ---------------------------
# Student Dashboard API
# ---------------------------
class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Only students can access this endpoint
        if not hasattr(user, 'studentprofile'):
            return Response({"detail": "Only students can access this."}, status=403)

        student = user.studentprofile

        # Get all fee categories assigned to the student's school
        fee_categories = FeeCategory.objects.filter(school=student.school)
        fee_list = []

        for fee in fee_categories:
            payments = Payment.objects.filter(student=student, category=fee)
            paid_amount = sum(p.amount for p in payments if p.status == 'success')
            fee_list.append({
                "category": fee.name,
                "amount_due": float(fee.amount),
                "amount_paid": float(paid_amount),
                "status": "Paid" if paid_amount >= fee.amount else "Pending",
                "payments": [
                    {
                        "amount": float(p.amount),
                        "method": p.method,
                        "status": p.status,
                        "reference": p.reference,
                        "paid_at": p.paid_at
                    } for p in payments
                ]
            })

        return Response({"fees": fee_list})


# ---------------------------
# Parent Dashboard API
# ---------------------------
class ParentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Only parents can access this endpoint
        if not hasattr(user, 'parentprofile'):
            return Response({"detail": "Only parents can access this."}, status=403)

        # All children of parent
        children = user.parentprofile.children.all()
        data = []

        for child in children:
            fee_categories = FeeCategory.objects.filter(school=child.school)
            fees = []
            for fee in fee_categories:
                payments = Payment.objects.filter(student=child, category=fee)
                paid_amount = sum(p.amount for p in payments if p.status == 'success')
                fees.append({
                    "category": fee.name,
                    "amount_due": float(fee.amount),
                    "amount_paid": float(paid_amount),
                    "status": "Paid" if paid_amount >= fee.amount else "Pending",
                    "payments": [
                        {
                            "amount": float(p.amount),
                            "method": p.method,
                            "status": p.status,
                            "reference": p.reference,
                            "paid_at": p.paid_at
                        } for p in payments
                    ]
                })
            data.append({
                "child_name": child.user.get_full_name(),
                "class": child.current_class.name,
                "fees": fees
            })

        return Response({"children": data})

def student_dashboard_template(request):
    # similar logic as API
    fees = []
    # populate fees
    return render(request, 'finance/student_dashboard.html', {'fees': fees})


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reference = request.data.get("reference")
        payment = Payment.objects.get(reference=reference)

        data = verify_paystack_payment(reference)

        if data["data"]["status"] == "success":
            payment.verified = True
            payment.save()

            invoice = payment.invoice
            invoice.amount_paid += payment.amount
            invoice.is_paid = invoice.amount_paid >= invoice.total_amount
            invoice.save()

            return Response({"status": "verified"})

        return Response({"status": "failed"}, status=400)



from rest_framework.viewsets import ModelViewSet
from core.permissions import IsAdminUserRole
from .models import FeeCategory
from .serializers import FeeCategorySerializer

class FeeViewSet(ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [IsAdminUserRole]


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_invoices(request):
    invoices = Invoice.objects.filter(student=request.user)
    return Response(InvoiceSerializer(invoices, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    invoice = Invoice.objects.get(reference=request.data["reference"])
    invoice.status = "paid"
    invoice.save()

    Payment.objects.create(
        invoice=invoice,
        amount=invoice.fee.amount,
        method="paystack",
        verified=True
    )

    return Response({"message": "Payment verified"})
