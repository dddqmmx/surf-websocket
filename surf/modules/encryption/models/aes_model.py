import hashlib
from abc import ABC

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, AEADDecryptionContext


class AESEncryption(ABC):

    def __init__(self, key):
        sha256_hash = hashlib.sha256()

        # 更新哈希对象以包含字节组
        sha256_hash.update(key)

        # 获取哈希值的十六进制表示
        self.key = sha256_hash.digest()

    def encrypt(self, data):
        # 使用AES算法，选择CBC模式
        cipher = Cipher(algorithms.AES256(self.key), modes.CBC(b'\x00' * 16), backend=default_backend())
        encryptor = cipher.encryptor()

        # 使用PKCS7填充方式进行填充
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        # 加密数据
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return ciphertext

    def decrypt(self, data):
        cipher = Cipher(algorithms.AES256(self.key), modes.CBC(b'\x00' * 16), backend=default_backend())
        decrypt: AEADDecryptionContext = cipher.decryptor()

        # 解密数据
        decrypted_data = decrypt.update(data) + decrypt.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data
