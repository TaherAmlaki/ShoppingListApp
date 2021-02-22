from flask import Flask

from ShoppingListApp.DB.mongodb import db

from ShoppingListApp.Views.user_views import user_views
from ShoppingListApp.Views.site import site

from ShoppingListApp import configs


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = configs.SECRET_KEY
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["MONGODB_SETTINGS"] = configs.MONGODB_SETTINGS

    db.init_app(app)

    app.register_blueprint(user_views)
    app.register_blueprint(site)

    return app

