from __future__ import annotations
from typing import Protocol

from cryptography.fernet import Fernet


class Encryptor(Protocol):
    def encrypt(self, plain_text: str) -> str:
        ...

    def decrypt(self, encrypted_text: str) -> str:
        ...


class FernetEncryptor(Encryptor):
    def __init__(self, key: str | bytes):
        if not key:
            raise RuntimeError("Encryption key is not set.")
        self._cipher = Fernet(key.encode() if isinstance(key, str) else key)

    def encrypt(self, plain_text: str) -> str:
        return self._cipher.encrypt(plain_text.encode("utf-8")).decode("utf-8")

    def decrypt(self, encrypted_text: str) -> str:
        return self._cipher.decrypt(encrypted_text.encode("utf-8")).decode("utf-8")