from django.db import models
from django.contrib.auth.models import User
import secrets
# Create your models here.


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # code = models.CharField(max_length=32, default=secrets.token_urlsafe(24))
    code=models.CharField(str(secrets.randbelow(10**8)),max_length=8)
    is_active = models.BooleanField(default=False)
           
        
    def __str__(self) -> str:
        return f"{self.user.username}"
