from typing import Protocol, List

from insurances import models as orm_model
from insurances.domain_model import Insurance


class InsuranceRepository(Protocol):

    def get(self, identifier: str) -> Insurance: ...

    def list(self) -> List[Insurance]: ...

    def save(self, insurance: Insurance) -> None: ...


class ORMInsuranceRepository:

    def get(self, identifier: str) -> Insurance:
        return orm_model.Insurance.objects.get(identifier=identifier).to_domain()

    def list(self) -> List[Insurance]:
        return [insurance.to_domain() for insurance in orm_model.Insurance.objects.all()]

    def save(self, insurance: Insurance) -> None:
        orm_model.Insurance.from_domain(insurance)
