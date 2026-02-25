from django.contrib import admin
from .models import FeeCategory, Invoice, Payment

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name',)
    list_filter = ('school',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'total_amount', 'amount_paid', 'is_paid', 'created_at')
    list_filter = ('is_paid',)
    search_fields = ('student__user__email', 'term')
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Only change: replace `category` with a method `get_fee` that points to invoice.fee
    list_display = ('invoice', 'get_fee', 'amount', 'method', 'verified', 'paid_at')
    list_filter = ('method', 'verified', 'invoice__fee')
    search_fields = ('invoice__student__user__email', 'invoice__fee__name', 'reference')
    ordering = ('-paid_at',)

    # Custom method to keep exactly the same admin look as before
    def get_fee(self, obj):
        return obj.invoice.fee.name
    get_fee.short_description = 'Fee'

