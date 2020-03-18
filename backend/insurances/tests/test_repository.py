from insurances.models import Insurance
from insurances.repository import ORMInsuranceRepository


def test_repo_can_save_insurance(session, insurance):
    repo = ORMInsuranceRepository()
    repo.save(insurance)

    saved_insurance = Insurance.objects.get(identifier=insurance.identifier)
    assert saved_insurance.identifier == 'Test'
    assert saved_insurance.car_id == 'ABC'
    assert saved_insurance.status == 'ACTIVE'
