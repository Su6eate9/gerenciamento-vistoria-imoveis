from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from flask import jsonify
import os
from utils.helpers import find_by_id

RELATORIOS_DB = []

class RelatorioService:
    @staticmethod
    def gerar_pdf(relatorio_id):
        relatorio = find_by_id(RELATORIOS_DB, relatorio_id)
        if not relatorio:
            return jsonify({"error": "Relatório não encontrado."}), 404

        # Caminho para salvar o PDF
        pdf_path = os.path.join("uploads", f"relatorio_{relatorio_id}.pdf")

        # Configurar o canvas do PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Adicionar informações do relatório
        c.drawString(100, 750, f"Relatório ID: {relatorio['id']}")
        c.drawString(100, 735, f"Vistoria ID: {relatorio['vistoria_id']}")
        c.drawString(100, 720, f"Vistoriador ID: {relatorio['vistoriador_id']}")
        c.drawString(100, 705, f"Data de Criação: {relatorio['data_criacao']}")
        c.drawString(100, 690, f"Observações: {relatorio['observacoes']}")

        # Adicionar fotos ao PDF
        y_position = 660
        for foto in relatorio.get("fotos", []):
            if os.path.exists(foto):
                c.drawImage(foto, 100, y_position, width=200, height=150)
                y_position -= 160  # Espaço entre fotos

        # Finalizar o PDF
        c.save()

        return jsonify({"message": "PDF gerado com sucesso.", "path": pdf_path}), 200
