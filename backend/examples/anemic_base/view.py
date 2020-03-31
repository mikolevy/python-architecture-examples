import datetime

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from infrastructure import response
from examples.anemic_base.model import Insurance, Pause

MAX_AVAILABLE_PAUSES = 3


@api_view(["POST"])
def hold(request: Request) -> Response:
    insurance_identifier = request.GET.get("insurance_identifier")
    insurance = Insurance.objects.filter(identifier=insurance_identifier)

    if len(insurance.pauses) >= MAX_AVAILABLE_PAUSES:
        return response.bad_request('Pause limit exceeded')

    if insurance.status not in [Insurance.Status.ACTIVE or Insurance.Status.IN_GREY_PERIOD]:
        return response.bad_request('Wrong insurance status')

    now = datetime.datetime.now()
    Pause.objects.create(insurance_identifier=insurance, begin_at=now)
    insurance.status = Insurance.Status.ON_HOLD
    insurance.save()

    return response.ok_no_content()


