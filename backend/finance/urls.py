from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    FeeCategoryViewSet,
    PaymentViewSet,
    StudentDashboardView,
    ParentDashboardView
)
from .views import my_invoices, verify_payment
# ---------------------------
# Router for ViewSets
# ---------------------------
router = DefaultRouter()
router.register('categories', FeeCategoryViewSet, basename='categories')
router.register('payments', PaymentViewSet, basename='payments')

# ---------------------------
# Additional API endpoints
# ---------------------------
urlpatterns = router.urls + [
    path('dashboard/student/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('dashboard/parent/', ParentDashboardView.as_view(), name='parent-dashboard'),
    path("my-invoices/", my_invoices),
    path("verify-payment/", verify_payment),

]

