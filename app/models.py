from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here

    class Meta:
        permissions = (
            ('readdir', 'can see dir and camera'),)
