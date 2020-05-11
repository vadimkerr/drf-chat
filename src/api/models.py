from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


# Message model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # make sure empty message text is not allowed
            models.CheckConstraint(check=~models.Q(text=""), name="non_empty_text")
        ]

    def __str__(self):
        return f"{self.pk}: {self.sender} -> {self.receiver}: {self.text[:20]}..."
