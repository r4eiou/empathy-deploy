from flask import Blueprint, render_template

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journal")
def page():
    return render_template("journal.html")
