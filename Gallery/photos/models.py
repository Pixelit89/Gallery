from django.db import models
from django.contrib.auth.models import User


class Images(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to="images/")