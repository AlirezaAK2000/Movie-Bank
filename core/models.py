from statistics import mode
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

class Movie(models.Model):
    name = models.CharField(max_length=150 ,unique=True ,blank=False)
    description = models.TextField(default="")
    rating = models.FloatField(
        default=0.0,
        validators=[
            MaxValueValidator(1.0),
            MinValueValidator(0.0)
        ]
    )

class Comment(models.Model):
    user = models.ForeignKey(get_user_model() ,on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie ,on_delete=models.CASCADE)
    comment_body = models.TextField(blank=False)
    approved = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    
class Vote(models.Model):
    user = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie ,on_delete=models.CASCADE)
    rating = models.FloatField(
        blank=False,
        validators=[
            MaxValueValidator(1.0),
            MinValueValidator(0.0)
        ]
    )
    