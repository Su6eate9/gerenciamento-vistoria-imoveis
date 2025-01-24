from flask import Blueprint, request, jsonify
from services.funcionario_service import FuncionarioService
from utils.decorators import autorizacao_permitida

funcionario_bp = Blueprint('funcionario', __name__)

@funcionario_bp.route('/funcionario', methods=['POST'])
@autorizacao_permitida(["Imobiliaria"])  # Apenas Imobiliarias podem criar funcionários
def create_funcionario():
    try:
        data = request.json
        # Validação dos dados recebidos
        if not data or not all(key in data for key in ["email", "telefone", "senha", "creci", "nome", "tipo"]):
            return jsonify({"error": "Dados incompletos para criar o funcionário."}), 400

        return FuncionarioService.create_funcionario(data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


@funcionario_bp.route('/funcionario/<int:id>/agendar_vistoria', methods=['POST'])
@autorizacao_permitida(["Imobiliaria", "Vistoriador"])  # Ambos os tipos podem agendar vistorias
def agendar_vistoria(id):
    try:
        data = request.json
        # Validação dos dados recebidos
        if not data or not all(key in data for key in ["vistoria_id", "data", "horario"]):
            return jsonify({"error": "Dados incompletos para agendar a vistoria."}), 400

        return FuncionarioService.agendar_vistoria(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


@funcionario_bp.route('/funcionario/<int:id>/reagendar_vistoria', methods=['PUT'])
@autorizacao_permitida(["Imobiliaria", "Vistoriador"])  # Ambos os tipos podem reagendar vistorias
def reagendar_vistoria(id):
    try:
        data = request.json
        # Validação dos dados recebidos
        if not data or not all(key in data for key in ["agendamento_id", "nova_data", "novo_horario"]):
            return jsonify({"error": "Dados incompletos para reagendar a vistoria."}), 400

        return FuncionarioService.reagendar_vistoria(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
