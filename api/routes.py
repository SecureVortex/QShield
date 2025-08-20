from fastapi import APIRouter
from quantum_entropy.entropy_manager import EntropyManager

router = APIRouter()

@router.get("/entropy")
def get_entropy(n: int = 32):
    manager = EntropyManager()
    return {"entropy": manager.get_entropy(n).hex()}
