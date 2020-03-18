from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.decorators import api_view

from infrastructure import response
from insurances import app_services
from insurances.domain_model import DomainLogicException
from insurances.repository import ORMInsuranceRepository
from location.proxy import current_location


@api_view(["POST"])
def resume_endpoint(request):
    repo = ORMInsuranceRepository()
    try:
        with transaction.atomic():
            app_services.resume(repo, current_location, request.data['identifier'])
    except DomainLogicException as error:
        return response.bad_request(str(error))
    except ObjectDoesNotExist:
        return response.not_found()
    return response.ok_no_content()
