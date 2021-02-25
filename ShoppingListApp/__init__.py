from flask import Flask

from ShoppingListApp.DB.mongodb import db

from ShoppingListApp.users.login import login_manager

from ShoppingListApp.users.views import user_views
from ShoppingListApp.site.views import site_views
from ShoppingListApp.shoppingLists.views import shopping_list_views

from ShoppingListApp.configs import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(user_views)
    app.register_blueprint(site_views)
    app.register_blueprint(shopping_list_views)

    return app

