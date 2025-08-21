from .qrng_interface import QRNGInterface

class EntropyManager:
    def __init__(self):
        self.qrng = QRNGInterface()

    def get_entropy(self, n=32):
        return self.qrng.get_random_bytes(n)
