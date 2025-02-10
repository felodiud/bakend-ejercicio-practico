from pydantic import BaseModel


class UpdateTasaRequest(BaseModel):
    idOp: int
    tasa: float
    email: str