from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Tenant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    date_started = models.DateField(null=True, blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    is_active = models.BooleanField(default=True)
    # optional link to an auth user account
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='tenant')

    def __str__(self):
        return self.name

    def balance(self):
        # total charges - total payments
        charges = Charge.objects.filter(tenant=self)
        total_charges = sum((c.total_amount() for c in charges), Decimal('0.00'))
        payments = Payment.objects.filter(tenant=self)
        total_payments = sum((p.amount for p in payments), Decimal('0.00'))
        return total_charges - total_payments


class Charge(models.Model):
    """Represents monthly charges for rent, water and electricity for a tenant for a specific month."""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='charges')
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    water_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    electric_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('tenant', 'year', 'month'),)
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.tenant} — {self.year}-{self.month:02d}"

    def total_amount(self):
        return (self.rent_amount or Decimal('0.00')) + (self.water_charge or Decimal('0.00')) + (self.electric_charge or Decimal('0.00'))

    def paid_amount(self):
        payments = self.payments.all()
        return sum((p.amount for p in payments), Decimal('0.00'))

    def is_paid(self):
        return self.paid_amount() >= self.total_amount()


class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = f"{self.charge}" if self.charge else "General"
        return f"Payment {self.amount} for {self.tenant} ({target})"
