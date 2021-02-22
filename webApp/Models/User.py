import bcrypt

from DB.mongodb import db


class User(db.Document):
    username = db.StringField(required=True, min_length=4, max_length=50, unique=True)
    password = db.StringField(required=True)

    @classmethod
    def find_by_username(cls, username) -> "User":
        return cls.objects().filter(username=username).first()

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    
    def match_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode("utf-8"))

    def __repr__(self):
        return f"User(username={self.username})"
