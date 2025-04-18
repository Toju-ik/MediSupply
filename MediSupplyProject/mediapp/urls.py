from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_purchase_order, name='create_order'),

]
