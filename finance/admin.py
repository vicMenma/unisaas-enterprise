from django.contrib import admin
from .models import FeeCategory, Invoice, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('date',)

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'university')
    list_filter = ('university',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'total_amount', 'paid_amount', 'status', 'due_date', 'university')
    list_filter = ('status', 'due_date', 'university')
    search_fields = ('student__matricule', 'description')
    inlines = [PaymentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'invoice', 'amount', 'payment_method', 'date', 'university')
    list_filter = ('payment_method', 'date', 'university')
    search_fields = ('reference', 'invoice__student__matricule')
