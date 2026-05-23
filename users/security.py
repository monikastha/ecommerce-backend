from cryptography.fernet import Fernet
import jwt
from django.conf import settings

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def create_token(payload):
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return cipher_suite.encrypt(
        token.encode()
    ).decode()


def decrypt_token(enc_token):
    try:
        dec = cipher_suite.decrypt(
            enc_token.encode()
        ).decode()

        payload = jwt.decode(
            dec,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )

        return {
            "status": True,
            "payload": payload
        }

    except:
        return {"status": False}