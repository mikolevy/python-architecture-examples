from django.db import models

from infrastructure.model_mappings import model_choices_from_enum
from insurances import domain_model
from insurances.domain_model import InsuranceStatus


class Pause(models.Model):
    insurance_identifier = models.ForeignKey(
        'Insurance', on_delete=models.CASCADE, related_name='pauses'
    )
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True)

    @staticmethod
    def from_domain(pause: domain_model.Pause) -> 'Pause':
        orm_pause, _ = Pause.objects.get_or_create(
            insurance_identifier=pause.insurance_identifier,
            begin_at=pause.begin_at,
            end_at=pause.end_at
        )
        return orm_pause

    def to_domain(self) -> domain_model.Pause:
        return domain_model.Pause(
            insurance_identifier=str(self.insurance_identifier),
            begin_at=self.begin_at,
            end_at=self.end_at
        )


class Insurance(models.Model):
    identifier = models.CharField(max_length=255)
    car_id = models.CharField(max_length=255)
    protection_end = models.DateTimeField()
    status = models.CharField(
        max_length=40, choices=model_choices_from_enum(InsuranceStatus)
    )

    @staticmethod
    def from_domain(insurance: domain_model.Insurance) -> 'Insurance':
        try:
            orm_insurance = Insurance.objects.get(identifier=insurance.identifier)
        except Insurance.DoesNotExist:
            orm_insurance = Insurance(identifier=insurance.identifier)

        orm_insurance.car_id = insurance.car_id
        orm_insurance.protection_end = insurance.protection_end
        orm_insurance.status = insurance.status.value
        orm_insurance.save()
        Pause.objects.filter(insurance=orm_insurance).delete()
        orm_insurance.refresh_from_db()
        orm_insurance.pauses.set([
            Pause.from_domain(pause) for pause in insurance.pauses
        ])
        return orm_insurance

    def to_domain(self) -> domain_model.Insurance:
        pauses = [pause.to_domain() for pause in self.pauses]
        return domain_model.Insurance(
            identifier=self.identifier,
            car_id=self.car_id,
            protection_end=self.protection_end,
            status=InsuranceStatus(self.status),
            pauses=pauses
        )
