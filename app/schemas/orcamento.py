from pydantic import BaseModel, Field

class EntradasMedicaoSchema(BaseModel):
    largura_vao_mm: float = Field(..., example=2015.0, description="Largura do vão em mm")
    altura_vao_mm: float = Field(..., example=1980.0, description="Altura do vão em mm")
    qtd_pecas: int = Field(..., example=7, description="Quantidade de painéis")
    cor_vidro: str = Field("Incolor", example="Incolor")
    espessura_vidro: str = Field("10mm", example="10mm Laminado")
    cor_aluminio: str = Field("RAL 9007", example="RAL 9007")