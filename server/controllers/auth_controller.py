from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from server.models.user import User
from server.extensions import db
from server.utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')
    email = data.get('email')

    if not username or not password or not password_confirmation or not email:
        return error_response("Username, email, password, and password confirmation are required.", 400)

    if password != password_confirmation:
        return error_response("Passwords do not match.", 400)

    if User.query.filter_by(username=username).first():
        return error_response("Username already exists.", 400)

    if User.query.filter_by(email=email).first():
        return error_response("Email already registered.", 400)

    try:
        new_user = User(username=username, email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return success_response({"token": access_token, "user": new_user.to_dict()}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating user: {str(e)}", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return error_response("Username and password are required.", 400)

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return error_response("Invalid username or password.", 401)

    access_token = create_access_token(identity=user.id)
    return success_response({"token": access_token, "user": user.to_dict()}, 200)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response("User not found.", 404)

    return success_response(user.to_dict(), 200)

@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    return success_response({}, 200)