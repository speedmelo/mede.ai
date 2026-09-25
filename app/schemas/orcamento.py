from pydantic import BaseModel, Field
from typing import Optional

class EntradasMedicaoSchema(BaseModel):
    tipo_calculo: str = Field(default="sacada_reta", description="sacada_reta, box_padrao ou sacada_l")
    largura_vao_mm: float = Field(..., gt=0, description="Largura total do vao em mm (ou Lado A)")
    largura_lado_b_mm: Optional[float] = Field(default=0.0, description="Largura do Lado B em mm (para Sacada em L)")
    altura_vao_mm: float = Field(..., gt=0, description="Altura total do vao em mm")
    qtd_pecas: int = Field(default=1, gt=0, description="Quantidade de paineis (Lado A)")
    qtd_pecas_lado_b: Optional[int] = Field(default=0, description="Quantidade de paineis Lado B")
    cor_vidro: str = Field(default="Incolor")
    espessura_vidro: str = Field(default="10mm")
    cor_aluminio: str = Field(default="Preto")
