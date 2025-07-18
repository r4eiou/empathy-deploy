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

@entry_bp.route("/entry/<entry_id>/toggle_favorite", methods=["POST"])
def toggle_favorite(entry_id):
    if "user_id" not in session:
        return redirect(url_for("auth.index"))

    entry = mongo.db.journal_entries.find_one({
        "_id": ObjectId(entry_id),
        "user_id": session["user_id"]
    })

    if not entry:
        flash("Entry not found.", "error")
        return redirect(url_for("allEntries.allEntries"))

    new_fav_status = not entry.get("isFavorite", False)

    mongo.db.journal_entries.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": {"isFavorite": new_fav_status}}
    )

    return {"success": True, "isFavorite": new_fav_status}