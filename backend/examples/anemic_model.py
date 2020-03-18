from django.db import models


class Pause(models.Model):
    insurance_identifier = models.ForeignKey(
        'Insurance', on_delete=models.CASCADE, related_name='pauses'
    )
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True)


class Insurance(models.Model):
    class Status:
        ACTIVE = 'ACTIVE'
        ON_HOLD = 'ON_HOLD'
        IN_GREY_PERIOD = 'IN_GREY_PERIOD'
        INACTIVE = 'INACTIVE'

    insurance_status_choices = (
        (Status.ACTIVE, Status.ACTIVE),
        (Status.ON_HOLD, Status.ON_HOLD),
        (Status.IN_GREY_PERIOD, Status.IN_GREY_PERIOD),
        (Status.INACTIVE, Status.INACTIVE),
    )

    identifier = models.CharField(max_length=255)
    car_id = models.CharField(max_length=255)
    protection_end = models.DateTimeField()
    status = models.CharField(
        max_length=40, choices=insurance_status_choices
    )


class Product(models.Model):
    description = models.TextField()
    image = models.ImageField()
    category_description = models.TextField()
    price = models.IntegerField()
    activated = models.BooleanField()

