import os 

from flask import Flask

from datetime import timedelta

from DB.mongodb import db

from Views.user_views import user_views
from Views.site import site

import configs


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = configs.SECRET_KEY
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_AUTH_URL_RULE"] = configs.JWT_AUTH_URL_RULE
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(hours=1)
    app.config["JWT_AUTH_USERNAME_KEY"] = configs.JWT_AUTH_USERNAME_KEY
    app.config["MONGODB_SETTINGS"] = configs.MONGODB_SETTINGS

    db.init_app(app)
    
    app.register_blueprint(user_views)
    app.register_blueprint(site)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000, host="0.0.0.0")
