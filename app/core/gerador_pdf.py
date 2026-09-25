import os
from reportlab.lib import colors
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

    # Cabeçalho - Empresa Logada
    c.setFont("Helvetica-Bold", 16)
    c.drawString(
        50,
        750,
        f"CONTRATO DE MEDIÇÃO & SERVIÇO - {dados_empresa.get('nome_fantasia', 'MEDE.AI').upper()}",
    )
    c.setFont("Helvetica", 10)
    c.drawString(
        50, 735, f"CNPJ: {dados_empresa.get('cnpj', '00.000.000/0001-00')}"
    )
    c.setStrokeColor(colors.HexColor("#1A1A1A"))
    c.setLineWidth(1)
    c.line(50, 725, 550, 725)

    # 1. Dados do Cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 700, "1. DADOS DO CLIENTE")
    c.setFont("Helvetica", 10)
    c.drawString(50, 685, f"Nome: {dados_cliente.get('nome', 'N/A')}")
    c.drawString(50, 670, f"WhatsApp: {dados_cliente.get('whatsapp', 'N/A')}")

    # 2. Especificações Técnicas
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 640, "2. ESPECIFICAÇÕES TÉCNICAS DA SACADA")
    c.setFont("Helvetica", 10)
    c.drawString(
        50,
        625,
        f"Vidro: {especificacoes.get('cor_vidro')} |"
        f" {especificacoes.get('espessura')}",
    )
    c.drawString(50, 610, f"Alumínio: {especificacoes.get('cor_aluminio')}")
    c.drawString(
        50,
        595,
        f"Medida do Vão: {resultado_corte.get('qtd_pecas')} painéis | Área:"
        f" {resultado_corte.get('area_total_m2')} m²",
    )

    # 3. Resumo do Corte de Fábrica
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 565, "3. CORTE DE FÁBRICA RECOMENDADO")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(
        50, 550, f"Resumo: {resultado_corte.get('medida_corte_fabrica')}"
    )

    # Assinaturas
    c.line(50, 480, 250, 480)
    c.drawString(50, 465, "Assinatura do Cliente")

    c.line(320, 480, 520, 480)
    c.drawString(
        320,
        465,
        f"Assinatura - {dados_empresa.get('nome_fantasia', 'Empresa')}",
    )

    c.save()
    return caminho_saida