from typing import Protocol, List

from fexample.insurance.domain_model import Insurance


class InsuranceRepository(Protocol):

    def get(self, reference: str) -> Insurance: ...

    def list(self) -> List[Insurance]: ...

    def add(self, insurance: Insurance) -> None: ...


class ORMInsuranceRepository:

    def __init__(self, session):
        self.session = session

    def get(self, identifier: str) -> Insurance:
        return self.session.query(Insurance).filter_by(identifier=identifier).one()

    def list(self) -> List[Insurance]:
        return self.session.query(Insurance).all()

    def add(self, insurance: Insurance) -> None:
        self.session.add(insurance)
