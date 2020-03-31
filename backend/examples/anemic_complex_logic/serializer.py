import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from examples.anemic_complex_logic.model import Pause, Insurance
from location.proxy import current_location

MAX_AVAILABLE_PAUSES = 3


class PauseSerializer(serializers.ModelSerializer):
    pause = serializers.BooleanField(default=False)

    class Meta:
        model = Pause
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["pause"]:
            ...
        validated_data["begin_at"] = datetime.datetime.now()
        validated_data["end_at"] = None
        insurance = Insurance.objects.get(identifier=validated_data["insurance_identifier"])
        insurance.status = Insurance.Status.ON_HOLD
        insurance.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["begin_at"] = instance.begin_at
        validated_data["end_at"] = datetime.datetime.now()
        insurance = Insurance.objects.get(identifier=validated_data["insurance_identifier"])
        insurance.status = Insurance.Status.ACTIVE
        insurance.save()
        return super().update(instance, validated_data)

    def validate(self, attrs):
        insurance = Insurance.objects.get(identifier=attrs["insurance_identifier"])
        if self.instance:
            if insurance.status is not Insurance.Status.ON_HOLD:
                raise ValidationError()
            location = current_location(insurance.car_id)
            if not(50 < location.latitude < 55 and 15 < location.longitude < 25):
                raise ValidationError()
        else:
            if len(insurance.pauses) >= MAX_AVAILABLE_PAUSES:
                raise ValidationError()
            if insurance.status is Insurance.Status.ON_HOLD:
                raise ValidationError()
            if insurance.status is Insurance.Status.INACTIVE:
                raise ValidationError()
        return attrs