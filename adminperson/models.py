from django.db import models
from django.conf import settings

class AdminPerson(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_person',
        limit_choices_to={'role': 'admin'},
        null=True,          # ← Temporarily allow null
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Admin Person"
        verbose_name_plural = "Admin Persons"
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"{self.user.name} ({self.user.username})"
        return "No User Assigned"