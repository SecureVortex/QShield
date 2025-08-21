import requests
import os

class QRNGInterface:
    def __init__(self):
        self.endpoint = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=hex16&size=32"

    def get_random_bytes(self, n):
        try:
            response = requests.get(self.endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "data" not in data:
                raise Exception("No 'data' key in QRNG response.")
            entropy_hex = data["data"][0]
            return (bytes.fromhex(entropy_hex), "quantum")
        except Exception as e:
            print("Error fetching QRNG entropy:", e)
            # Fallback: use local OS entropy for now
            return (os.urandom(n), "fallback")
