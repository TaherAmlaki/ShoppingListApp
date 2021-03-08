from flask import session
from wtforms.fields.core import DecimalField
from typing import Dict
from decimal import Decimal


def load_previous_data_to_add_shopping_list(form):
    previous_data: Dict = session.get("AddShoppingListData", None)
    if previous_data:
        form.name.data = previous_data.get("name")
        previous_data.pop("csrf_token", None)
        previous_data.pop("name", None)
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
