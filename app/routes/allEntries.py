from flask import Blueprint, session, redirect, url_for, render_template, request, flash

all_entries_bp = Blueprint("allEntries", __name__)

@all_entries_bp.route("/allEntries", methods=["GET", "POST"])
def allEntries():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    
    return render_template("allEntries.html")
