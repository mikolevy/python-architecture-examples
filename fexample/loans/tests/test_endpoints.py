import json
from unittest.mock import patch

from fexample.loans.repository import ORMInsuranceRepository


def test_resume_insurance_happy_path(client, insurance, session, allowed_location):
    insurance.hold()

    ORMInsuranceRepository(session).add(insurance)
    session.commit()
    with patch('fexample.loans.endpoints.current_location', return_value=allowed_location):
        result = client.post('loans/resume', data=json.dumps({
            'identifier': insurance.identifier
        }), content_type='application/json')
    assert result.status_code == 204


def test_resume_insurance_unhappy_path(client, insurance, session, allowed_location):
    ORMInsuranceRepository(session).add(insurance)
    session.commit()

    with patch('fexample.loans.endpoints.current_location', return_value=allowed_location):
        result = client.post('loans/resume', data=json.dumps({
            'identifier': insurance.identifier
        }), content_type='application/json')
    assert result.status_code == 400
