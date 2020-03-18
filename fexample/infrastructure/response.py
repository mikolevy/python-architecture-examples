from flask import jsonify


def ok_no_content():
    return '', 204


def not_found():
    return jsonify({'message': 'Non existing entity'}), 404


def bad_request(message: str):
    return jsonify({'message': message}), 400
