import rsa
import socket
from Crypto.Cipher import AES
import json
from base64 import b64encode, b64decode
import os


class EncryptionManger:
    def __init__(self, sock):
        self.sock = sock
        self.aes_key = None
        self.private_key = rsa.PrivateKey.load_pkcs1(os.getenv('PRIVATE_KEY').encode())

    def recv(self):
        if self.aes_key is None:
            self.aes_key = self.recv_rsa()
            return b'<SYMMETRIC KEY EXCHANGE>'
        else:
            return self.recv_aes()

    def recv_rsa(self) -> bytes:
        msg = self._rsa_decryption(self.sock.recv(256))
        if len(msg) != 24:
            return None
        return msg

    def recv_aes(self) -> bytes:
        try:
            length = int(self.sock.recv(8))
            msg = self.sock.recv(length)
            return self._aes_decryption(msg)
        except ValueError:
            return None

    def send_aes(self, data: bytes) -> None:
        msg = self._aes_encryption(data)
        self.sock.sendall(str(len(msg)).zfill(8).encode())
        self.sock.sendall(msg)

    def _rsa_decryption(self, msg):
        try:
            return rsa.decrypt(msg, self.private_key)
        except rsa.pkcs1.DecryptionError as e:
            return None

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


encryption_dict: dict[socket.socket, EncryptionManger] = {}