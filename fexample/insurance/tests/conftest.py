import datetime

import pytest

from fexample.insurance.domain_model import Datetime, Insurance, InsuranceStatus
from fexample.location.data_model import Location


@pytest.fixture
def allowed_location() -> Location:
    return Location(latitude=53, longitude=20)


@pytest.fixture
def not_allowed_location() -> Location:
    return Location(latitude=10, longitude=5)


@pytest.fixture
def next_year() -> Datetime:
    return datetime.datetime.now() + datetime.timedelta(days=365)


@pytest.fixture
def after_10_min() -> Datetime:
    return datetime.datetime.now() + datetime.timedelta(minutes=10)


@pytest.fixture
def insurance(next_year) -> Insurance:
    return Insurance(
        identifier='Test',
        car_id='ABC',
        protection_end=next_year,
        status=InsuranceStatus.ACTIVE,
    )
