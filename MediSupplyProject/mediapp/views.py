from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PurchaseOrder
from .forms import PurchaseOrderForm

@login_required
def create_purchase_order(request):
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            return redirect('order_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'mediapp/create_order.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PurchaseOrder

@login_required
def order_list(request):
    user = request.user
    if user.role == 'staff':
        orders = PurchaseOrder.objects.filter(created_by=user)
    elif user.role == 'manager':
        orders = PurchaseOrder.objects.filter(status='Pending')
    elif user.role == 'supplier':
        orders = PurchaseOrder.objects.filter(status='Approved')
    else:  # admin
        orders = PurchaseOrder.objects.all()

    return render(request, 'mediapp/order_list.html', {
        'orders': orders
    })
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def approve_order(request, order_id):
    order = get_object_or_404(PurchaseOrder, pk=order_id, status='Pending')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            order.status = 'Approved'
            messages.success(request, f"Order {order_id} approved.")
        elif action == 'reject':
            order.status = 'Rejected'
            messages.warning(request, f"Order {order_id} rejected.")
        order.save()
        return redirect('order_list')
    return render(request, 'mediapp/approve_order.html', {'order': order})

@login_required
def supplier_update(request, order_id):
    order = get_object_or_404(PurchaseOrder, pk=order_id, status='Approved')
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Shipped', 'Delivered']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order_id} marked as {new_status}.")
        return redirect('order_list')
    return render(request, 'mediapp/supplier_update.html', {'order': order})

