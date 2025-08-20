from .qrng_interface import QRNGInterface

class EntropyManager:
    """Manages quantum entropy for cryptographic operations."""

    def __init__(self):
        self.qrng = QRNGInterface()

    def get_entropy(self, n=32):
        """Return n bytes of quantum entropy."""
        return self.qrng.get_random_bytes(n)
