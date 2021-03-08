from flask import session
from wtforms.fields.core import DecimalField
from typing import Dict
from decimal import Decimal


def load_previous_data_to_add_shopping_list(form):
    previous_data: Dict = session.get("AddShoppingListData", None)
    if previous_data is None or previous_data.get("action", None) not in ['add', 'remove']:
        return form 
    elif previous_data.get('action', "nothing") == "add":
        previous_data.pop("action", None)
        return add_new_item_to_shopping_form(form, previous_data)
    elif previous_data.get('action', "nothing") == "remove":
        previous_data.pop("action", None)
        return remove_item_from_shopping_list(form, previous_data)


def remove_item_from_shopping_list(form, previous_data):
    if previous_data:
        form.name.data = previous_data.get("name")
        previous_data.pop("csrf_token", None)
        previous_data.pop("name", None)
        _, removed_item_index = previous_data['itemIndex'].split("-")
        removed_item_index = int(removed_item_index)
        previous_data.pop("itemIndex", None)
        for key, val in previous_data.items():
            if "csrf_token" in key:
                continue
            _, item_ind, prop = key.split("-")
            item_ind = int(item_ind)

            try:
                if item_ind < removed_item_index:
                    item = form.items[item_ind]
                elif item_ind == removed_item_index:
                    continue
                else:
                    item = form.items[item_ind-1] 
            except IndexError:
                continue
            else:
                p = getattr(item, prop, None)
                if p:
                    if isinstance(p, DecimalField):
                        val = Decimal(val)
                    setattr(p, "data", val) 

        session["AddShoppingListData"] = None
    return form


def add_new_item_to_shopping_form(form, previous_data):
    if previous_data:
        form.name.data = previous_data.get("name")
        previous_data.pop("csrf_token", None)
        previous_data.pop("name", None)
        previous_data.pop("itemIndex", None)
        for key, val in previous_data.items():
            if "csrf_token" in key:
                continue
            _, item_ind, prop = key.split("-")
            try:
                item = form.items[int(item_ind)]
                p = getattr(item, prop, None)
                if p:
                    if isinstance(p, DecimalField):
                        val = Decimal(val)
                    setattr(p, "data", val)
            except IndexError:
                continue
        session["AddShoppingListData"] = None
    return form