from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Wallet:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey().export_key().decode()
        self.private_key = self.key.export_key().decode()

    def sign_message(self, message):
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(self.key).sign(h)
        return signature

    @staticmethod
    def verify_message(message, signature, public_key):
        key = RSA.import_key(public_key)
        h = SHA256.new(message.encode())
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
