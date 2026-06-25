from django.db import models


class CommissionSettings(models.Model):
    """
    Global earnings settings for the platform.
    Admin can configure commission rates and delivery charges here.
    """

    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text="Commission percentage (e.g., 10 means 10%)",
    )
    normal_delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=200.00,
        help_text="Standard delivery charge in Rs.",
    )
    emergency_delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500.00,
        help_text="Emergency/Fast delivery charge in Rs.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Commission Settings"

    def __str__(self):
        return (
            f"Commission: {self.commission_rate}% | "
            f"Normal Delivery: Rs.{self.normal_delivery_charge} | "
            f"Emergency: Rs.{self.emergency_delivery_charge}"
        )

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(id=1)
        return settings
