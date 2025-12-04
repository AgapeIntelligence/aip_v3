#!/usr/bin/env python3
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib, os

def encrypt_quantum_seed(seed_bytes: bytes, password: bytes) -> dict:
    key = HKDF(hashlib.sha256, 32, salt=b"AIP_salt", info=b"AES_vault").derive(password)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, seed_bytes, None)
    return {"nonce": nonce.hex(), "ciphertext": ct.hex()}

def decrypt_quantum_seed(enc: dict, password: bytes) -> bytes:
    key = HKDF(hashlib.sha256, 32, salt=b"AIP_salt", info=b"AES_vault").derive(password)
    aes = AESGCM(key)
    return aes.decrypt(bytes.fromhex(enc["nonce"]), bytes.fromhex(enc["ciphertext"]), None)
