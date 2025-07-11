from flask import Blueprint, session, redirect, url_for, render_template

dash_bp = Blueprint("dashboard", __name__)

@dash_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    return render_template("dashboard.html")
