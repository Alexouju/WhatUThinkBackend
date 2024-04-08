import bcrypt


class User:
    def __init__(self, username, email, password=None, admin=False):
        self.username = username
        self.email = email
        self.admin = admin
        self.password_hash = password

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'password_hash': self.password_hash
        }

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
