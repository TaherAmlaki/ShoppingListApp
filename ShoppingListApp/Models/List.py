from datetime import datetime
from typing import List

from ShoppingListApp.DB.mongodb import db
from ShoppingListApp.Models.Item import Item
from ShoppingListApp.Models.User import User


def datetime_formatted():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%d %H:%M")


class ShoppingList(db.Document):
    name = db.StringField(required=True, max_length=50)
    created = db.DateTimeField(required=True, default=datetime_formatted)
    updated = db.DateTimeField()
    status = db.StringField(required=True, default="created", choices=["created", "editing", "closed"])
    user = db.ReferenceField(User)
    items = db.ListField(db.EmbeddedDocumentField(Item))

    @classmethod
    def find_by_name(cls, name) -> "ShoppingList":
        return cls.objects(name=name).order_by('-updated', '-created').first()

    @classmethod
    def find_by_id(cls, pk) -> "ShoppingList":
        return cls.objects(pk=pk).order_by('-updated', '-created').first()

    @classmethod
    def find_by_status(cls, status) -> List["ShoppingList"]:
        return cls.objects(status=status).order_by('-updated', '-created')

    @classmethod
    def find_by_user_id(cls, user_id) -> "ShoppingList":
        user = User.find_by_id(user_id)
        return cls.objects(user=user).order_by('-updated', '-created')

    @classmethod
    def get_paginator(cls, user_id, page_number):
        user = User.find_by_id(user_id)
        return cls.objects(user=user).order_by('-updated', '-created').paginate(page=page_number, per_page=5)

    def __repr__(self):
        return f"ShoppingList(id={self.id}, name={self.name}, created={self.created},status={self.status})"
