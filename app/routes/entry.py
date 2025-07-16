from flask import Blueprint, session, redirect, url_for, render_template, flash
from app.extensions import mongo 
from bson import ObjectId

entry_bp = Blueprint("entry", __name__)

@entry_bp.route("/entry/<entry_id>", methods=["GET", "POST"])
def entry(entry_id):
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    
    entry = mongo.db.journal_entries.find_one({
        "_id": ObjectId(entry_id),
        "user_id": session["user_id"]
    })

    if not entry:
        flash("Enntry not found.", "error")
        return redirect(url_for("allEntries.allEntries"))

    return render_template("entry.html", entry=entry)


@entry_bp.route("/entry/<entry_id>/delete", methods=["POST"])
def delete_entry(entry_id):
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    
    result = mongo.db.journal_entries.delete_one({
        "_id": ObjectId(entry_id),
        "user_id": session["user_id"]
    })

    if result.deleted_count == 0:
        flash("Entry could not be deleted or was not found.", "error")
    else:
        flash("Entry deleted successfully.", "success")
    
    return redirect(url_for("allEntries.allEntries"))