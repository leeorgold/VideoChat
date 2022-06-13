import rsa
import socket
from Crypto.Cipher import AES
import json
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes


with open(r'..\..\public.pem', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())


class EncryptionManger:
    public_key = public_key

    def __init__(self, ip: str, port=10000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.aes_key = get_random_bytes(24)
        self.send_key()

    def send_key(self):
        self.sock.sendall(rsa.encrypt(self.aes_key, self.public_key))

    def recv(self) -> bytes:
        try:
            length = int(self.sock.recv(8))
            msg = self.sock.recv(length)
            return self._aes_decryption(msg)
        except ValueError:
            return None

    def send(self, data: bytes) -> None:
        msg = self._aes_encryption(data)
        self.sock.sendall(str(len(msg)).zfill(8).encode())
        self.sock.sendall(msg)

    def _aes_encryption(self, msg):
        assert type(msg) is bytes, f"Expected type {bytes!r}. Got {type(msg)!r}."
        eax = AES.new(self.aes_key, AES.MODE_EAX)
        ciphertext, tag = eax.encrypt_and_digest(msg)
        json_k = ['nonce', 'ciphertext', 'tag']
        json_v = [b64encode(x).decode('utf-8') for x in (eax.nonce, ciphertext, tag)]
        return json.dumps(dict(zip(json_k, json_v))).encode()

    def _aes_decryption(self, msg):
        try:
            dictionary = json.loads(msg)
            valid_keys = ('nonce', 'ciphertext', 'tag')
            if len(dictionary) != len(valid_keys):
                raise KeyError(f'Expected 3 items. {len(valid_keys)} given.')
            for k in dictionary.keys():
                if k not in valid_keys:
                    raise KeyError(f'Unexpected key {k!r}')
                dictionary[k] = b64decode(dictionary[k])
            eax = AES.new(self.aes_key, AES.MODE_EAX, nonce=dictionary['nonce'])
            return eax.decrypt_and_verify(dictionary['ciphertext'], dictionary['tag'])
        except (KeyError, ValueError):
            return None
