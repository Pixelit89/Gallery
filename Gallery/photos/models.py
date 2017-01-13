from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    image = models.ImageField(upload_to='/media/images/')
