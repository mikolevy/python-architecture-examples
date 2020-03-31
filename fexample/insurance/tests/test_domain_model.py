import pytest

from fexample.insurance.domain_model import InsuranceStatus, MAX_AVAILABLE_PAUSES, PauseLimitExceeded, \
    WrongStateForAction, CarLocationNotAllowed, PauseAlreadyFinished, UnableToHoldInactive, UnableToHoldOnHold


def test_hold_insurance(insurance):
    insurance.hold()
    assert insurance.status is InsuranceStatus.ON_HOLD


def test_unable_to_hold_when_exceeded_pause_limit(insurance, allowed_location):
    for _ in range(MAX_AVAILABLE_PAUSES):
        insurance.hold()
        insurance.resume(allowed_location)

    with pytest.raises(PauseLimitExceeded):
        insurance.hold()


def test_unable_to_hold_when_already_on_hold(insurance):
    insurance.hold()

    with pytest.raises(UnableToHoldOnHold):
        insurance.hold()


def test_unable_to_hold_when_in_inactive_status(insurance):
    insurance.status = InsuranceStatus.INACTIVE

    with pytest.raises(UnableToHoldInactive):
        insurance.hold()


def test_resume_insurance(insurance, allowed_location):
    insurance.hold()
    insurance.resume(allowed_location)

    assert insurance.status is InsuranceStatus.ACTIVE


def test_unable_to_resume_when_not_on_hold(insurance, allowed_location):
    with pytest.raises(WrongStateForAction):
        insurance.resume(allowed_location)


def test_unable_to_resume_when_outside_the_allowed_location(insurance, not_allowed_location):
    insurance.hold()

    with pytest.raises(CarLocationNotAllowed):
        insurance.resume(not_allowed_location)


def test_pause_for_constant_period_when_exceeded_pause_limit(insurance, allowed_location):
    for _ in range(MAX_AVAILABLE_PAUSES):
        insurance.hold()
        insurance.resume(allowed_location)

    insurance.pause()

    assert insurance.status is InsuranceStatus.ON_HOLD


def test_unable_to_resume_pause(insurance, allowed_location):
    insurance.pause()

    with pytest.raises(PauseAlreadyFinished):
        insurance.resume(allowed_location)


def test_unable_to_pause_when_in_grey_period(insurance):
    insurance.status = InsuranceStatus.IN_GREY_PERIOD

    with pytest.raises(WrongStateForAction):
        insurance.pause()


def test_pause_not_overlap_on_grey_period(insurance, after_10_min):
    insurance.protection_end = after_10_min

    insurance.pause()

    assert insurance.pauses[-1].end_at == after_10_min
