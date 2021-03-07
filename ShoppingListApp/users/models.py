import bcrypt
from flask_login import UserMixin

from ShoppingListApp.DB.mongodb import db
from ShoppingListApp.users.login import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


class User(db.Document, UserMixin):
    username = db.StringField(required=True, min_length=4, max_length=50, unique=True)
    password = db.StringField(required=True)

    @classmethod
    def find_by_username(cls, username) -> "User":
        return cls.objects(username=username).first()

    @classmethod
    def find_by_id(cls, pk) -> "User":
        return cls.objects(pk=pk).first()

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    
    def match_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode("utf-8"))

    def __repr__(self):
        return f"User(username={self.username}, id={self.id})"

    def __eq__(self, other):
        try:
            return self.id == other.id 
        except AttributeError:
            return False 

    def __hash__(self):
        return hash(self.id)
         
