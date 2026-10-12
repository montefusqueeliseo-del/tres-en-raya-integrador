from pydantic import BaseModel, Field, field_validator


class PartidaCrear(BaseModel):
    jugador: str = Field(min_length=1, max_length=30)

    @field_validator("jugador")
    @classmethod
    def validar_jugador(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("El nombre no puede estar vacío")

        return valor


class JugadaCrear(BaseModel):
    partida_id: int = Field(gt=0)
    posicion: int = Field(ge=1, le=9)
    simbolo: str

    @field_validator("simbolo")
    @classmethod
    def validar_simbolo(cls, valor):
        valor = valor.strip().upper()

        if valor not in ["X", "O"]:
            raise ValueError("El símbolo debe ser X u O")

        return valor


class EstadoActualizar(BaseModel):
    estado: str

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor):
        estados_validos = ["en curso", "X ganó", "O ganó", "empate"]

        if valor not in estados_validos:
            raise ValueError("El estado no es válido")

        return valor