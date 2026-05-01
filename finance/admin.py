from django.contrib import admin
from .models import FeeCategory, Invoice, Payment


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'university')
    search_fields = ('name',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'description', 'total_amount', 'paid_amount', 'status', 'due_date')
    list_filter = ('status',)
    search_fields = ('description', 'student__matricule')
    readonly_fields = ('paid_amount', 'status')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'invoice', 'amount', 'payment_method', 'date')
    search_fields = ('reference',)
    readonly_fields = ('date',)
