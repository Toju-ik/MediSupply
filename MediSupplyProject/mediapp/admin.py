from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PurchaseOrder, OrderItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter  = ('role', 'is_active', 'is_staff')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'created_by', 'date_created', 'status', 'total_amount')
    list_filter  = ('status', 'date_created')
    search_fields = ('created_by__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'purchase_order', 'description', 'quantity', 'price')
    list_filter  = ('purchase_order',)
    search_fields = ('description',)

