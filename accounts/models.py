from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from conf.settings import EXPIRATION_TIME_EMAIL


# Create your models here.

class VerifyCodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=4)
    is_active = models.BooleanField(default=False)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}: {self.code}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = timezone.now() + timedelta(minutes=EXPIRATION_TIME_EMAIL)
        super().save(*args, **kwargs)
