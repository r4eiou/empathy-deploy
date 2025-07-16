from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from app.extensions import mongo
from bson import ObjectId


all_entries_bp = Blueprint("allEntries", __name__)

@all_entries_bp.route("/allEntries", methods=["GET", "POST"])
def allEntries():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    
    #fetching all entries of the logged user
    entries = list(
        mongo.db.journal_entries.find({"user_id": session["user_id"]}).sort("date", -1)
    )
    
    return render_template("allEntries.html", entries=entries)
