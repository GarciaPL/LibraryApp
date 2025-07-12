from flask import Blueprint, redirect

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    return redirect("/apidocs")
