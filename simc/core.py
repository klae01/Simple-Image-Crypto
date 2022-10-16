import argparse
import hashlib
import io
import os
import pathlib
from getpass import getpass

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image


def encrypt(path, encryptor):
    with open(path, "rb") as fp:
        data = fp.read()
    os.system(f"shred -u -n 2 '{path}'")
    pad_cand = list(range(256))
    pad_cand.pop(data[-1])
    padding = bytes([pad_cand[os.urandom(1)[0] % 255]]) * (16 - len(data) % 16)
    data = encryptor.update(data) + encryptor.update(padding) + encryptor.finalize()
    with open(path, "wb") as fp:
        fp.write(data)


def decrypt(path, decryptor):
    with open(path, "rb") as fp:
        data = fp.read()
    data = decryptor.update(data) + decryptor.finalize()
    image = Image.open(io.BytesIO(data.rstrip(bytes(data[-1:]))))
    image.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, choices=["enc", "dec"])
    parser.add_argument("path", type=pathlib.Path)
    args = parser.parse_args()

    hash_string = hashlib.sha3_384(getpass().encode()).digest()
    key, iv = hash_string[:32], hash_string[32:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    if args.type == "enc":
        encrypt(args.path, cipher.encryptor())
    elif args.type == "dec":
        decrypt(args.path, cipher.decryptor())
    else:
        raise NotImplementedError()


if __name__ == " __main__":
    main()
