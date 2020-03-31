import datetime
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List

from fexample.location.data_model import Location


class DomainLogicException(Exception):
    pass


class PauseLimitExceeded(DomainLogicException):
    pass


class WrongStateForAction(DomainLogicException):
    pass


class UnableToHoldInactive(DomainLogicException):
    pass


class UnableToHoldOnHold(DomainLogicException):
    pass


class PauseAlreadyFinished(DomainLogicException):
    pass


class CarLocationNotAllowed(DomainLogicException):
    pass


Datetime = datetime.datetime
now = datetime.datetime.now()

GREY_PERIOD_TIME = datetime.timedelta(days=5)
PAUSE_TIME = datetime.timedelta(days=1)
MAX_AVAILABLE_PAUSES = 3


class InsuranceStatus(Enum):
    ACTIVE = auto()
    ON_HOLD = auto()
    IN_GREY_PERIOD = auto()
    INACTIVE = auto()


@dataclass
class Pause:
    insurance_identifier: str
    begin_at: Datetime
    end_at: Optional[Datetime] = None

    def finish(self):
        if self.end_at:
            raise PauseAlreadyFinished()
        self.end_at = now


@dataclass
class Insurance:
    identifier: str
    car_id: str
    protection_end: Datetime
    status: InsuranceStatus
    pauses: List[Pause] = field(default_factory=list)

    def hold(self):
        if len(self.pauses) >= MAX_AVAILABLE_PAUSES:
            raise PauseLimitExceeded()

        if self.status is InsuranceStatus.ON_HOLD:
            raise UnableToHoldOnHold()

        if self.status is InsuranceStatus.INACTIVE:
            raise UnableToHoldInactive()

        self.pauses.append(Pause(insurance_identifier=self.identifier, begin_at=now))
        self.status = InsuranceStatus.ON_HOLD

    def resume(self, current_location: Location):
        if self.status is not InsuranceStatus.ON_HOLD:
            raise WrongStateForAction()

        if not self._is_location_allowed(current_location):
            raise CarLocationNotAllowed()

        last_pause = self.pauses[-1]
        last_pause.finish()
        self.status = self._subscription_status()

    def pause(self):
        if self.status is not InsuranceStatus.ACTIVE:
            raise WrongStateForAction()

        pause_end = now + PAUSE_TIME
        if pause_end > self.protection_end:
            pause_end = self.protection_end

        self.pauses.append(Pause(insurance_identifier=self.identifier, begin_at=now, end_at=pause_end))
        self.status = InsuranceStatus.ON_HOLD

    def _is_location_allowed(self, location: Location) -> bool:
        return 50 < location.latitude < 55 and 15 < location.longitude < 25

    def _subscription_status(self):
        if now <= self.protection_end:
            return InsuranceStatus.ACTIVE
        if self.protection_end < now <= self.protection_end + GREY_PERIOD_TIME:
            return InsuranceStatus.IN_GREY_PERIOD
        return InsuranceStatus.INACTIVE

    def __eq__(self, other):
        if not isinstance(other, Insurance):
            return False
        return other.identifier == self.identifier


# Domain service
def calculate_installment(car_type, driver_age, driver_area):
    ...


def calculate_loyalty_reword():
    ...
