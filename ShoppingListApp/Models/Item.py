from ShoppingListApp.DB.mongodb import db


class Item(db.EmbeddedDocument):
    name = db.StringField(required=True, max_length=50)
    price = db.FloatField(min_value=0.0)
    shop = db.StringField(max_length=20)

    @classmethod
    def find_by_name(cls, name):
        return cls.objects().filter(name=name).first()

