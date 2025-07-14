from flask import Blueprint, session, redirect, url_for, render_template

entry_bp = Blueprint("entry", __name__)

@entry_bp.route("/entry", methods=["GET", "POST"])
def entry():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    
    return render_template("entry.html")
