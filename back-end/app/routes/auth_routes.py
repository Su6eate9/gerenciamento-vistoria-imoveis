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
    """
    Endpoint para autenticação de usuários.
    """
    try:
        data = request.json
        if not data or "numero" not in data or "senha" not in data:
            return create_response(400, "Credenciais incompletas.")
        return AuthService.login(data)
    except Exception as e:
        return create_response(500, f"Erro inesperado: {str(e)}")


@auth_bp.route('/auth/recover', methods=['POST'])
def recover_password():
    """
    Endpoint para envio de e-mail de recuperação de senha.
    """
    try:
        data = request.json
        if not data or "email" not in data:
            return create_response(400, "E-mail é obrigatório.")
        return AuthService.recover_password(data)
    except Exception as e:
        return create_response(500, f"Erro inesperado: {str(e)}")


@auth_bp.route('/recover-password/<token>', methods=['POST'])
def reset_password(token):
    """
    Endpoint para redefinir a senha de um usuário.
    """
    try:
        data = request.json
        if not data or "new_password" not in data:
            return create_response(400, "Nova senha é obrigatória.")
        return AuthService.reset_password(token, data)
    except Exception as e:
        return create_response(500, f"Erro inesperado: {str(e)}")