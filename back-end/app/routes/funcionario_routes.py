from flask import Blueprint, request
from services.funcionario_service import FuncionarioService

funcionario_bp = Blueprint('funcionario', __name__)

@funcionario_bp.route('/funcionario', methods=['POST'])
def create_funcionario():
    return FuncionarioService.create_funcionario(request.json)

@funcionario_bp.route('/funcionario/<int:id>/agendar_vistoria', methods=['POST'])
def agendar_vistoria(id):
    return FuncionarioService.agendar_vistoria(id, request.json)

@funcionario_bp.route('/funcionario/<int:id>/reagendar_vistoria', methods=['PUT'])
def reagendar_vistoria(id):
    return FuncionarioService.reagendar_vistoria(id, request.json)
