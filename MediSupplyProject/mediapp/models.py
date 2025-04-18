from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Hospital Staff'),
        ('manager', 'Purchasing Manager'),
        ('supplier', 'Supplier'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return self.username

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    order_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.order_id} by {self.created_by.username}"


class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='order_items')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price per unit

    def __str__(self):
        return f"{self.description} (x{self.quantity})"

