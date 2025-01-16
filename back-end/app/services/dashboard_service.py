from flask import jsonify
from utils.pagination import paginate

class DashboardService:
    @staticmethod
    def listar_vistorias(params):
        # Lógica para buscar todas as vistorias com paginação
        data = []  # Substituir com os dados reais
        paginated_data = paginate(data, params)
        return jsonify(paginated_data)
