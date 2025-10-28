from django.contrib import admin
from .models import Tenant, Charge, Payment
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "date_started", "formatted_monthly_rent", "is_active", "has_account")
    search_fields = ("name",)
    actions = ("create_user_account",)

    def has_account(self, obj):
        # Prefer explicit linked user when present
        if getattr(obj, 'user', None):
            return True
        username = f"tenant_{obj.pk}"
        return User.objects.filter(username=username).exists()
    has_account.boolean = True
    has_account.short_description = "Has account"

    def create_user_account(self, request, queryset):
        created = 0
        skipped = 0
        for tenant in queryset:
            username = f"tenant_{tenant.pk}"
            if User.objects.filter(username=username).exists():
                skipped += 1
                continue
            # create a user with unusable password; admin can set password later
            user = User.objects.create_user(username=username, email="")
            user.set_unusable_password()
            # set a readable display name in first/last name if possible
            parts = tenant.name.split(None, 1)
            if parts:
                user.first_name = parts[0]
                if len(parts) > 1:
                    user.last_name = parts[1]
            user.save()
            # link tenant -> user
            tenant.user = user
            tenant.save()
            created += 1
        msg = []
        if created:
            msg.append(f"Created {created} user account(s).")
        if skipped:
            msg.append(f"Skipped {skipped} existing account(s).")
        self.message_user(request, " ".join(msg), level=messages.INFO)
    create_user_account.short_description = "Create user account(s) for selected tenants"

    def formatted_monthly_rent(self, obj):
        try:
            return f"₱{obj.monthly_rent:,.2f}"
        except Exception:
            return obj.monthly_rent
    formatted_monthly_rent.short_description = "Monthly Rent"
    formatted_monthly_rent.admin_order_field = "monthly_rent"


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ("tenant", "year", "month", "formatted_total_amount")
    list_filter = ("year", "month")
    search_fields = ("tenant__name",)

    def formatted_total_amount(self, obj):
        try:
            return f"₱{obj.total_amount():,.2f}"
        except Exception:
            return obj.total_amount()
    formatted_total_amount.short_description = "Total"
    formatted_total_amount.admin_order_field = None


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("tenant", "formatted_amount", "date", "charge")
    search_fields = ("tenant__name",)

    def formatted_amount(self, obj):
        try:
            return f"₱{obj.amount:,.2f}"
        except Exception:
            return obj.amount
    formatted_amount.short_description = "Amount"
    formatted_amount.admin_order_field = "amount"
