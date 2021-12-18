from django.db import models


class Newsletter(models.Model):
    class Meta:
        verbose_name = "Newsletter Signup"
        verbose_name_plural = "Newsletter Signups"

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    code = models.CharField(unique=True, max_length=35)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        else:
            return f"{self.email}"

    def admin_user_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"-"
