from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, abort, request, jsonify, session
from flask_login import current_user, login_required
from wtforms import FieldList, FormField
from flask_restful import Api

from .models import Item
from .forms import ShoppingList, AddShoppingListForm, AddItemForm
from .helpers import load_previous_data_to_add_shopping_list
from .resources import ModifyShoppingListResource, basket_market_object
from ShoppingListApp.users.models import User


shopping_list_views = Blueprint("shopping_list_views", 
                                __name__, 
                                url_prefix="/shopping-lists", 
                                template_folder='templates')

shopping_list_api = Api(shopping_list_views)
shopping_list_api.add_resource(ModifyShoppingListResource, "/modify_add_shopping_list")


@shopping_list_views.route("/add", methods=["POST", "GET"])
@login_required
def add_shopping_list():
    num_items = request.args.get('items', default=0, type=int)
    AddShoppingListForm.items = FieldList(FormField(AddItemForm), min_entries=num_items)

    form = AddShoppingListForm()
    form = load_previous_data_to_add_shopping_list(form)

    if form.validate_on_submit():
        list_obj = ShoppingList()
        list_obj.name = form.name.data
        list_obj.status = "created"
        list_obj.user = User.find_by_id(current_user.get_id())

        items = []
        for item in form.items:
            item_obj = Item()
            item_obj.name = item.item_name.data
            item_obj.price = float(item.price.data)
            item_obj.shop = str(item.shop.data)
            items.append(item_obj)
        list_obj.items = items
        list_obj.save()

        basket_market_object.reset()
        basket_market_object.set_user_id(current_user.get_id())
        basket_market_object.process()

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
    
    basket_market_object.reset()
    basket_market_object.set_user_id(current_user.get_id())
    basket_market_object.process()

    flash(f"Deleted '{the_list.name}' successfully.", "info")
    return redirect(url_for("site_views.home"))


@shopping_list_views.route("/frequent-itemsets")
@login_required
def get_frequent_item_sets():
    if not current_user.is_authenticated:
        abort(401)
    if current_user.get_id() != basket_market_object.user_id:
        basket_market_object.reset_and_process(current_user.get_id())

    freq_item_sets = basket_market_object.frequent_item_sets
    return render_template("shoppingLists/frequent_item_sets.html", 
                           title="Frequently Bought Items", 
                           freq_item_sets=freq_item_sets)


@shopping_list_views.route("/patterns")
@login_required
def get_rules():
    if not current_user.is_authenticated:
        abort(401)
    if current_user.get_id() != basket_market_object.user_id:
        basket_market_object.reset_and_process(current_user.get_id())

    rules = basket_market_object.rules
    return render_template("shoppingLists/rules.html", 
                           title="Shopping List Patterns", 
                           rules=rules)
