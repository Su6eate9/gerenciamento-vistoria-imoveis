from flask import Blueprint, request, jsonify
from services.imobiliaria_service import ImobiliariaService

imobiliaria_bp = Blueprint('imobiliaria', __name__)

@imobiliaria_bp.route('/imobiliaria/<int:id>/desativar_imovel', methods=['PUT'])
def desativar_imovel(id):
    try:
        data = request.json
        if not data or "imovel_id" not in data:
            return jsonify({"error": "O campo 'imovel_id' é obrigatório."}), 400

        return ImobiliariaService.desativar_imovel(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@imobiliaria_bp.route('/imobiliaria/<int:id>/ativar_imovel', methods=['PUT'])
def ativar_imovel(id):
    try:
        data = request.json
        if not data or "imovel_id" not in data:
            return jsonify({"error": "O campo 'imovel_id' é obrigatório."}), 400

        return ImobiliariaService.ativar_imovel(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@imobiliaria_bp.route('/imobiliaria/<int:id>/cancelar_vistoria', methods=['PUT'])
def cancelar_vistoria(id):
    try:
        data = request.json
        if not data or "vistoria_id" not in data:
            return jsonify({"error": "O campo 'vistoria_id' é obrigatório."}), 400

        return ImobiliariaService.cancelar_vistoria(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
