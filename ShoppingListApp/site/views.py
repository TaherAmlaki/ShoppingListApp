from flask import Blueprint, render_template, request
from flask_login import current_user

from ShoppingListApp.shoppingLists.forms import ShoppingList

site_views = Blueprint("site_views",
                       __name__,
                       template_folder='templates')


@site_views.route("/")
@site_views.route("/home")
def home():
    paginator = []
    if current_user.is_authenticated:
        page_number = request.args.get('page', 1, type=int)
        paginator = ShoppingList.get_paginator(current_user.get_id(), page_number)
    return render_template("site/home.html", title="Home Page", paginator=paginator)
