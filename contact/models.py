from django.contrib.auth.models import User
from django.db import models

CONTACT_CHOICES = (
    ('custom-order', 'Custom Order'),
    ('general', 'General'),
    ('review', 'Review'),
    ('suggestion', 'Suggestion'),
    ('catering-request', 'Catering Request')
)


class Contact(models.Model):
    class Meta:
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    reason = models.CharField(choices=CONTACT_CHOICES, max_length=20)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()}'s Contact Request"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    get_full_name.short_description = "Full Name"
