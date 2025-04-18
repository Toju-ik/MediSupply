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
