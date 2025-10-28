from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Користувач'),
       
        ('admin', 'Адміністратор'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
