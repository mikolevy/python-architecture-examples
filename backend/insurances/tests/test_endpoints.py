import json
from unittest.mock import patch

from django.urls import reverse

from insurances.repository import ORMInsuranceRepository


def test_resume_insurance_happy_path(client, insurance, allowed_location):
    insurance.hold()

    ORMInsuranceRepository().save(insurance)
    with patch('insurance.endpoints.current_location', return_value=allowed_location):
        result = client.post(
            reverse('insurance-resume'),
            data=json.dumps({'identifier': insurance.identifier}),
            content_type='application/json'
        )
    assert result.status_code == 204


def test_resume_insurance_unhappy_path(client, insurance, allowed_location):
    ORMInsuranceRepository().save(insurance)

    with patch('insurance.endpoints.current_location', return_value=allowed_location):
        result = client.post(
            reverse('insurance-resume'),
            data=json.dumps({'identifier': insurance.identifier}),
            content_type='application/json'
        )
    assert result.status_code == 400
