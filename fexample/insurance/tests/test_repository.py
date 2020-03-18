from fexample.insurance.repository import ORMInsuranceRepository


def test_repo_can_save_insurance(session, insurance):
    repo = ORMInsuranceRepository(session)
    repo.add(insurance)
    session.commit()

    rows = list(session.execute(
        'SELECT identifier, car_id, status FROM "insurance"'
    ))
    assert rows == [("Test", "ABC", 'ACTIVE')]