from flask import Blueprint
from flask import render_template


site = Blueprint("site", __name__)


@site.route("/")
def home():
    return render_template("home.html", title="Home Page")



