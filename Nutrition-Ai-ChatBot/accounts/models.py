from django.contrib.auth.models import User
from django.db import models


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, )
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
    food_options = models.CharField(max_length=10,
                                    choices=[('veg', 'Veg'), ('non_veg', 'Non-Veg')],
                                    blank=True)
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary: Little or no exercise'),
        ('light', 'Light: Exercise 1-3 times/week'),
        ('moderate', 'Moderate: Exercise 4-5 times/week'),
        ('active', 'Active: Daily exercise or intense exercise 3-4 times/week'),
        ('very_active', 'Very Active: Intense exercise 6-7 times/week'),
    ]
    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES,
        default='sedentary',
    )
