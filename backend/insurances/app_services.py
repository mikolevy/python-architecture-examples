from insurances.repository import InsuranceRepository
from location.proxy import LocationProxy


def resume(repo: InsuranceRepository, current_location: LocationProxy, identifier: str):
    insurance = repo.get(identifier)
    location = current_location(insurance.car_id)
    insurance.resume(location)
    repo.save(insurance)
