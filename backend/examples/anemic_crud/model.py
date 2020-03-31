from django.db import models


class Product(models.Model):
    description = models.TextField()
    image = models.ImageField()
    category_description = models.TextField()
    price = models.IntegerField()
    activated = models.BooleanField()

