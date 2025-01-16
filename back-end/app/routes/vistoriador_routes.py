from flask import Blueprint, request
from services.vistoriador_service import VistoriadorService

vistoriador_bp = Blueprint('vistoriador', __name__)

@vistoriador_bp.route('/vistoriador/<int:id>/registrar_inspecao', methods=['POST'])
def registrar_inspecao(id):
    return VistoriadorService.registrar_inspecao(id, request.json)
