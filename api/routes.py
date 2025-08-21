from fastapi import APIRouter, Request, HTTPException, Depends
from quantum_entropy.entropy_manager import EntropyManager
import numpy as np
import os

API_KEY = os.environ.get("QSHIELD_API_KEY", "dev-secret")  # Set this in your environment for production

router = APIRouter()
manager = EntropyManager()

def check_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

@router.get("/entropy")
def get_entropy(n: int = 32, request: Request = None):
    check_api_key(request)
    value, source = manager.get_entropy(n)
    return {"entropy": value.hex(), "source": source}

@router.get("/detect")
def detect_anomaly(n: int = 32, threshold: float = 0.2, request: Request = None):
    check_api_key(request)
    value, source = manager.get_entropy(n)
    arr = np.frombuffer(value, dtype=np.uint8) / 255.0
    mean = arr.mean()
    anomaly = mean < threshold or mean > (1 - threshold)
    return {
        "anomaly_detected": anomaly,
        "anomaly_score": float(mean),
        "entropy": value.hex(),
        "source": source,
        "threshold": threshold
    }

@router.get("/simulate_attack")
def simulate_attack(strength: float = 0.5, request: Request = None):
    check_api_key(request)
    # Simulate: higher strength => higher success chance
    import random
    success = random.random() < strength
    desc = "Quantum attack succeeded" if success else "Quantum attack failed"
    return {
        "attack_success": success,
        "description": desc,
        "strength": strength
    }

@router.get("/healthz")
def health():
    return {"status": "ok"}
