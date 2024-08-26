import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from freedomlib.crypto.crypto_algorithm import CryptoAlgorithm

class AesGcm(CryptoAlgorithm):
    
    NONCE_SIZE: int = 12
    
    def __init__(self, nonce_size: int = NONCE_SIZE) -> None:
        self._nonce_size = nonce_size
    
    def encrypt(self, key: bytes, plaintext: bytes) -> tuple:
        nonce = os.urandom(self._nonce_size)

        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce)).encryptor()
        
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        return ciphertext, nonce, encryptor.tag
    
    def decrypt(self, key: bytes, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce, tag)).decryptor()
        
        return decryptor.update(ciphertext) + decryptor.finalize()