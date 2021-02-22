from datetime import datetime

from DB.mongodb import db
from Item import Item


class ShoppingList(db.Document):
    name = db.StringField(max_length=20)
    created = db.DateField(required=True, default=datetime.utcnow)
    updated = db.DateField()
    status = db.StringField(required=True, default="created", choices=["created", "editting", "closed"])
    items = db.EmbeddedDocumentListField(Item) 

    @classmethod
    def find_by_name(cls, name):
        return cls.objects().filter(name=name).first()

    @classmethod
    def find_by_status(cls, status):
        return cls.objects().filter(status=status)

