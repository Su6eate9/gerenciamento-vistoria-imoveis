from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

def create_response(status, message, data=None):
    """
    Helper para criar respostas padronizadas.
    """
    return jsonify({"status": status, "message": message, "data": data}), status


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            return create_response(400, "Credenciais incompletas.")
        return AuthService.login(data)
    except Exception as e:
        return create_response(500, f"Erro inesperado: {str(e)}")


@auth_bp.route('/auth/recover', methods=['POST'])
def recover_password():
    try:
        data = request.json
        if not data or "email" not in data:
            return create_response(400, "E-mail é obrigatório.")
        return AuthService.recover_password(data)
    except Exception as e:
        return create_response(500, f"Erro inesperado: {str(e)}")


@auth_bp.route('/recover-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        data = request.json
        if not data or "new_password" not in data:
            return create_response(400, "Nova senha é obrigatória.")
        return AuthService.reset_password(token, data)
    except Exception as e:
        return create_response(500, f"Erro inesperado: {str(e)}")
