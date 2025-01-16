from flask import Blueprint, request
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/vistorias', methods=['GET'])
def listar_vistorias():
    return DashboardService.listar_vistorias(request.args)
