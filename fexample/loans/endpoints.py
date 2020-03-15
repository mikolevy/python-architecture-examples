from flask import request, jsonify, Blueprint
from sqlalchemy.orm.exc import NoResultFound

from fexample.db import db_session
from fexample.location.proxy import current_location
from fexample.loans import app_services
from fexample.loans.domain_model import DomainLogicException
from fexample.loans.repository import ORMInsuranceRepository

loans = Blueprint('loans', __name__, url_prefix='/loans')


@loans.route("/resume", methods=['POST'])
def resume_endpoint():
    repo = ORMInsuranceRepository(db_session)
    try:
        app_services.resume(repo, current_location, request.json['identifier'])
        db_session.commit()
    except DomainLogicException as error:
        db_session.rollback()
        return jsonify({'message': str(error)}), 400
    except NoResultFound:
        db_session.rollback()
        return jsonify({'message': 'Non existing entity'}), 404
    return '', 204
