from bcrypt import hashpw, gensalt, checkpw
from django.conf import settings

class Encrypt:
    def __init__(self, string, encrypted_string=''):
        self.string = string
        self.encrypted_string = encrypted_string

    def get_encrypted_string(self):
        if self.encrypted_string:
            return self.encrypted_string
        string_in_bytes = self.string.encode('utf-8')
        salt = gensalt(rounds=settings.PASSWORD_ENCRYPTION_STRENGTH)
        encrypted_string_in_bytes = hashpw(string_in_bytes, salt)
        encrypted_string = encrypted_string_in_bytes.decode()
        self.encrypted_string = encrypted_string
        return self.encrypted_string

    def compare_encrypted_values(self):
        return checkpw(self.string.encode('utf-8'), self.encrypted_string.encode('utf-8'))

# test = Encrypt('123456')
# print()