from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from server.models.user import User
from server.extensions import db
from server.utils.responses import (success_response, error_response)
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')

    if not username or not password or not password_confirmation:
        return error_response("Username, password, and password confirmation are required.", 400)

    if password != password_confirmation:
        return error_response("Passwords do not match.", 400)

    if User.query.filter_by(username=username).first():
        return error_response("Username already exists.", 400)

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return success_response({"token": access_token, "user": {"id": new_user.id, "username": new_user.username}}, 201)

