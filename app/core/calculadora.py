from typing import Dict, Any

class CalculadoraVidro:
    """
    Motor de cálculo de engenharia técnica para envidraçamento de sacadas.
    Aplica os descontos de folga para altura (-16cm), acabamento e borrachas.
    """

    @staticmethod
    def calcular_pecas_sacada_reta(
        largura_vao_mm: float,
        altura_vao_mm: float,
        qtd_pecas: int,
        desconto_altura_cm: float = 16.0,
        folga_acabamento_parede_cm: float = 3.0,
        folga_borracha_mm: float = 3.0
    ) -> Dict[str, Any]:
        
        # 1. Conversão para milímetros
        desconto_altura_mm = desconto_altura_cm * 10.0
        acabamento_parede_mm = folga_acabamento_parede_cm * 10.0
        
        # 2. Altura final do vidro (-16cm por padrão)
        altura_vidro_final = altura_vao_mm - desconto_altura_mm
        
        # 3. Largura útil com folga de borrachas e acabamento
        total_folga_borrachas_mm = folga_borracha_mm * qtd_pecas
        largura_util_mm = largura_vao_mm - acabamento_parede_mm - total_folga_borrachas_mm
        largura_vidro_final = largura_util_mm / qtd_pecas
        
        # 4. Área Total em m²
        area_total_m2 = (largura_vao_mm / 1000.0) * (altura_vao_mm / 1000.0)

        return {
            "resumo": f"{qtd_pecas} PC LAM",
            "largura_peca_mm": round(largura_vidro_final, 1),
            "altura_peca_mm": round(altura_vidro_final, 1),
            "qtd_pecas": qtd_pecas,
            "area_total_m2": round(area_total_m2, 2),
            "medida_corte_fabrica": f"{qtd_pecas} peças de {round(largura_vidro_final, 1)}mm x {round(altura_vidro_final, 1)}mm"
        }