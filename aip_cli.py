#!/usr/bin/env python3
import argparse, json, getpass
import numpy as np
from aip_core import generate_quantum_ris
from aip_identity import derive_quantum_identity
from aip_vault import encrypt_quantum_seed, decrypt_quantum_seed

def main():
    parser = argparse.ArgumentParser(description="AIP v3 CLI")
    parser.add_argument("--gen", action="store_true", help="Generate new quantum RIS")
    parser.add_argument("--encrypt", type=str, help="Encrypt seed with password")
    parser.add_argument("--decrypt", type=str, help="Decrypt vault JSON with password")
    parser.add_argument("--biometric", type=str, help="Optional path to biometric flux npy file")
    args = parser.parse_args()

    flux = None
    if args.biometric:
        flux = np.load(args.biometric).astype(np.float32)

    if args.gen:
        ris = generate_quantum_ris(flux)
        ident = derive_quantum_identity(ris["quantum_spinor"])
        print(json.dumps(ident, indent=2))

    if args.encrypt:
        password = getpass.getpass("Vault password: ").encode()
        enc = encrypt_quantum_seed(args.encrypt.encode(), password)
        print(json.dumps(enc, indent=2))

    if args.decrypt:
        password = getpass.getpass("Vault password: ").encode()
        enc_json = json.loads(args.decrypt)
        dec = decrypt_quantum_seed(enc_json, password)
        print("Decrypted seed:", dec.decode())

if __name__ == "__main__":
    main()
