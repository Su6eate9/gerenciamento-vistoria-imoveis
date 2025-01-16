from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    return AuthService.login(request.json)

@auth_bp.route('/auth/recover', methods=['POST'])
def recover_password():
    return AuthService.recover_password(request.json)

@auth_bp.route('/recover-password/<token>', methods=['POST'])
def reset_password(token):
    return AuthService.reset_password(token, request.json)
