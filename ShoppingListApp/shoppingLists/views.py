from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, abort
from flask_login import current_user, login_required

from .models import Item
from .forms import ShoppingList, AddShoppingListForm
from ShoppingListApp.users.models import User


shopping_list_views = Blueprint("shopping_list_views", 
                                __name__, 
                                url_prefix="/shopping_list", 
                                template_folder='templates')


@shopping_list_views.route("/new", methods=["POST", "GET"])
@login_required
def add_shopping_list():
    form = AddShoppingListForm()
    if form.validate_on_submit():
        list_obj = ShoppingList()
        list_obj.name = form.name.data
        list_obj.status = "created"
        list_obj.user = User.find_by_id(current_user.get_id())

        items = []
        for item in form.items:
            item_obj = Item()
            item_obj.name = item.name
            item_obj.price = float(item.price.data)
            item_obj.shop = str(item.shop.data)
            items.append(item_obj)
        list_obj.items = items
        list_obj.save()
        flash("New shopping list is saved.", 'info')
        return redirect(url_for("site_views.home"))
    return render_template("shoppingLists/add_shopping_list.html", title="Add Shopping List", form=form)


@shopping_list_views.route("/details/<list_id>")
@login_required
def detail_shopping_list(list_id):
    the_list = ShoppingList.find_by_id(list_id)
    if the_list is None:
        abort(404)
    elif the_list.user != current_user:
        print("users are not equal")
        abort(403)

    the_list.created = datetime.strftime(the_list.created, "%Y-%m-%d %H:%M")
    if the_list.updated:
        the_list.updated = datetime.strftime(the_list.updated, "%Y-%m-%d %H:%M")
    return render_template("shoppingLists/detail_shopping_list.html", title="Detail Shopping List", the_list=the_list)
   

@shopping_list_views.route("/delete/<list_id>", methods=["POST"])
@login_required
def delete_shopping_list(list_id):
    the_list = ShoppingList.find_by_id(list_id)
    if the_list and the_list.user != current_user:
        abort(403)

    the_list.delete()
    flash(f"Deleted '{the_list.name}' successfully.", "info")
    return redirect(url_for("site_views.home"))
