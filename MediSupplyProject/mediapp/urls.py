from django.urls import path, include
from . import views

urlpatterns = [

    # 1. Create a new purchase order
    path('create-order/', views.create_purchase_order, name='create_order'),

    # 2. List orders (role-based)
    path('orders/', views.order_list, name='order_list'),

    # 3. Review (approve/reject) a specific order by ID
    path('orders/<int:order_id>/review/', views.approve_order, name='approve_order'),

    # 4. Supplier updates a specific order's status
    path('orders/<int:order_id>/update/', views.supplier_update, name='supplier_update'),

    # 5. Let users hit the "Add Items" page
path('orders/<int:order_id>/items/', views.add_order_items, name='add_order_items'),
]
