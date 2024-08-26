from abc import ABC, abstractmethod


class CryptoAlgorithm(ABC):
    
    @abstractmethod
    def encrypt(self, key: bytes, plaintext: bytes) -> tuple:
        ...

    @abstractmethod
    def decrypt(self, key: bytes, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
        ...