from flask import Blueprint, request
from services.notificacao_service import NotificacaoService

notificacao_bp = Blueprint('notificacao', __name__)

@notificacao_bp.route('/notificacoes', methods=['GET'])
def listar_notificacoes():
    destinatario_id = request.args.get("destinatario_id")
    if not destinatario_id:
        return {"error": "destinatario_id é obrigatório"}, 400
    return NotificacaoService.listar_notificacoes(int(destinatario_id))

@notificacao_bp.route('/notificacoes/<int:id>', methods=['PUT'])
def marcar_como_lida(id):
    return NotificacaoService.marcar_como_lida(id)
