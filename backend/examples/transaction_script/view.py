import datetime

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from infrastructure import response

MAX_AVAILABLE_PAUSES = 3


def _get_db_connection():
    from unittest.mock import Mock
    return Mock()


class InsuranceStatus:
    ACTIVE = 'ACTIVE'
    ON_HOLD = 'ON_HOLD'
    IN_GREY_PERIOD = 'IN_GREY_PERIOD'
    INACTIVE = 'INACTIVE'


@api_view(["POST"])
def hold(request: Request) -> Response:
    insurance_identifier = request.GET.get("insurance_identifier")
    db = _get_db_connection()

    number_of_pauses = db.query("SELECT COUNT(*) FROM pauses WHERE insurance_identifier = ...")
    insurance_status = db.query("SELECT status FROM insurance WHERE insurance_identifier = ...")

    if number_of_pauses >= MAX_AVAILABLE_PAUSES:
        return response.bad_request('Pause limit exceeded')

    if insurance_status not in [InsuranceStatus.ACTIVE or InsuranceStatus.IN_GREY_PERIOD]:
        return response.bad_request('Wrong insurance status')

    now = datetime.datetime.now()
    db.execute("INSERT INTO pauses (insurance_identifier, begin_at) VALUE ...")
    db.execute("UPDATE insurance SET status = ...")

    return response.ok_no_content()





