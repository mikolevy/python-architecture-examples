from typing import List

from fexample.loans import app_services
from fexample.loans.domain_model import Insurance, InsuranceStatus


class InMemoryInsuranceRepository:

    def __init__(self, insurances: List[Insurance]):
        self._insurances = insurances

    def get(self, identifier: str) -> Insurance:
        return next(
            insurance for insurance in self._insurances if insurance.identifier == identifier
        )

    def list(self) -> List[Insurance]:
        return self._insurances

    def add(self, insurance: Insurance) -> None:
        if insurance in self._insurances:
            self._insurances.remove(insurance)
        self._insurances.append(insurance)


def test_resume_make_insurance_active(insurance, allowed_location):
    insurance.hold()
    repo = InMemoryInsuranceRepository([insurance])

    app_services.resume(repo, lambda car_id: allowed_location, insurance.identifier)

    assert repo.get(insurance.identifier).status is InsuranceStatus.ACTIVE
