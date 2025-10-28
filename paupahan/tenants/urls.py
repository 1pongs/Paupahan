from django.urls import path
from . import views

app_name = "tenants"

urlpatterns = [
    path("", views.tenant_list, name="list"),
    path("tenants/add/", views.tenant_create, name="tenant_add"),
    path("tenants/<int:pk>/", views.tenant_detail, name="tenant_detail"),
    path("tenants/<int:pk>/edit/", views.tenant_edit, name="tenant_edit"),
    path("charges/add/", views.charge_create, name="charge_add"),
    path("payments/add/", views.payment_create, name="payment_add"),
]
