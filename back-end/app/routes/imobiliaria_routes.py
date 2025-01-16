from flask import Blueprint, request
from services.imobiliaria_service import ImobiliariaService

imobiliaria_bp = Blueprint('imobiliaria', __name__)

@imobiliaria_bp.route('/imobiliaria/<int:id>/desativar_imovel', methods=['PUT'])
def desativar_imovel(id):
    return ImobiliariaService.desativar_imovel(id, request.json)

@imobiliaria_bp.route('/imobiliaria/<int:id>/ativar_imovel', methods=['PUT'])
def ativar_imovel(id):
    return ImobiliariaService.ativar_imovel(id, request.json)

@imobiliaria_bp.route('/imobiliaria/<int:id>/cancelar_vistoria', methods=['PUT'])
def cancelar_vistoria(id):
    return ImobiliariaService.cancelar_vistoria(id, request.json)
