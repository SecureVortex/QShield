from pydantic import BaseModel

class EntropyRequest(BaseModel):
    n: int = 32
