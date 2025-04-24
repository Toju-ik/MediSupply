# mediapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import PurchaseOrder
from .forms import PurchaseOrderForm, OrderItemFormSet


@login_required
def create_purchase_order(request):
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            # Redirect immediately to the items form
            return redirect('add_order_items', order_id=order.order_id)
    else:
        form = PurchaseOrderForm()
    return render(request, 'mediapp/create_order.html', {'form': form})


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
    # Allow updating if order is Approved or already Shipped
    order = get_object_or_404(
        PurchaseOrder,
        pk=order_id,
        status__in=['Approved', 'Shipped']
    )
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Shipped', 'Delivered']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order_id} marked as {new_status}.")
        return redirect('order_list')

    return render(request, 'mediapp/supplier_update.html', {
        'order': order
    })


@login_required
def add_order_items(request, order_id):
    order = get_object_or_404(PurchaseOrder, pk=order_id, created_by=request.user)
    formset = OrderItemFormSet(request.POST or None, instance=order)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        # Recalculate total_amount
        total = sum(item.quantity * item.price for item in order.order_items.all())
        order.total_amount = total
        order.save()
        return redirect('order_list')

    return render(request, 'mediapp/add_items.html', {
        'order': order,
        'formset': formset
    })
