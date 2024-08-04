from django.contrib.auth.models import User
from django.db import models


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20,)
    email = models.EmailField(blank=True)
    height = models.FloatField(null=True, blank=True)  # Height in meters
    weight = models.FloatField(null=True, blank=True)  # Weight in kilograms
    age = models.PositiveIntegerField(null=True, blank=True)  # Age in years
    goal = models.CharField(max_length=20,
                            choices=[('loss', 'Weight Loss'), ('gain', 'Weight Gain'),
                                     ('maintain', 'Weight Maintenance')], blank=True)
    gender = models.CharField(max_length=10,
                              choices=[('male', 'Male'), ('female', 'Female')],
                              blank=True)
