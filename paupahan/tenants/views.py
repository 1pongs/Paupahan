from django.shortcuts import render, get_object_or_404, redirect
from .models import Tenant, Charge
from .forms import TenantForm, ChargeForm, PaymentForm
from django.urls import reverse
from django.utils import timezone


def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, "tenants/tenant_list.html", {"tenants": tenants})


def tenant_detail(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    charges = tenant.charges.order_by('-year', '-month')
    payments = tenant.payments.order_by('-date')
    return render(request, "tenants/tenant_detail.html", {"tenant": tenant, "charges": charges, "payments": payments})


def tenant_create(request):
    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            t = form.save()
            return redirect(reverse("tenants:tenant_detail", args=[t.pk]))
    else:
        form = TenantForm()
    return render(request, "tenants/tenant_form.html", {"form": form})


def tenant_edit(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == "POST":
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect(reverse("tenants:tenant_detail", args=[tenant.pk]))
    else:
        form = TenantForm(instance=tenant)
    return render(request, "tenants/tenant_form.html", {"form": form, "tenant": tenant})


def charge_create(request):
    if request.method == "POST":
        form = ChargeForm(request.POST)
        if form.is_valid():
            c = form.save()
            return redirect(reverse("tenants:tenant_detail", args=[c.tenant.pk]))
    else:
        # allow pre-filling tenant and default month/year from query params
        initial = {}
        tenant_id = request.GET.get('tenant')
        if tenant_id:
            initial['tenant'] = tenant_id
        now = timezone.now()
        initial.setdefault('year', now.year)
        initial.setdefault('month', now.month)
        form = ChargeForm(initial=initial)
    return render(request, "tenants/charge_form.html", {"form": form})


def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            p = form.save()
            return redirect(reverse("tenants:tenant_detail", args=[p.tenant.pk]))
    else:
        form = PaymentForm()
    return render(request, "tenants/payment_form.html", {"form": form})
