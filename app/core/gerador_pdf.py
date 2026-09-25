import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class GeradorContratoPDF:

  @staticmethod
  def gerar_pdf_orcamento(
      caminho_saida: str,
      dados_empresa: dict,
      dados_cliente: dict,
      especificacoes: dict,
      resultado_corte: dict,
  ) -> str:
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(
        50,
        750,
        f"CONTRATO DE SERVICO - {dados_empresa.get('nome_fantasia', 'MEDE.AI').upper()}",
    )
    c.setFont("Helvetica", 10)
    c.drawString(
        50, 735, f"CNPJ: {dados_empresa.get('cnpj', '00.000.000/0001-00')}"
    )
    c.line(50, 725, 550, 725)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 700, "1. DADOS DO CLIENTE")
    c.setFont("Helvetica", 10)
    c.drawString(50, 685, f"Nome: {dados_cliente.get('nome', 'N/A')}")
    c.drawString(50, 670, f"WhatsApp: {dados_cliente.get('whatsapp', 'N/A')}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 640, "2. ESPECIFICACOES TECNICAS DA SACADA")
    c.setFont("Helvetica", 10)
    c.drawString(
        50,
        625,
        f"Vidro: {especificacoes.get('cor_vidro')} |"
        f" {especificacoes.get('espessura')}",
    )
    c.drawString(50, 610, f"Aluminio: {especificacoes.get('cor_aluminio')}")
    c.drawString(
        50,
        595,
        f"Medida do Vao: {resultado_corte.get('qtd_pecas')} paineis | Area:"
        f" {resultado_corte.get('area_total_m2')} m2",
    )
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 565, "3. CORTE DE FABRICA RECOMENDADO")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(
        50, 550, f"Resumo: {resultado_corte.get('medida_corte_fabrica')}"
    )
    c.line(50, 500, 250, 500)
    c.drawString(50, 485, "Assinatura do Cliente")
    c.line(320, 500, 520, 500)
    c.drawString(320, 485, "Assinatura do Tecnico / Empresa")
    c.save()
    return caminho_saida