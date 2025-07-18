from flask import Blueprint, session, redirect, url_for, render_template, request, flash, jsonify
from app.extensions import mongo
from bson import ObjectId


all_entries_bp = Blueprint("allEntries", __name__)

@all_entries_bp.route("/allEntries", methods=["GET", "POST"])
def allEntries():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    
    #fetching all entries of the logged user
    entries = list(
        mongo.db.journal_entries.find({"user_id": session["user_id"]}).sort([
            ("isFavorite", -1),  # favorites first (True > False)
            ("date", -1)         # then by date descending
        ])
    )
    
    return render_template("allEntries.html", entries=entries)


@all_entries_bp.route("/toggle_favorite/<entry_id>", methods=["POST"])
def toggle_favorite(entry_id):
    if "user_id" not in session:
        return {"success": False, "error": "Unauthorized"}, 401

    entry = mongo.db.journal_entries.find_one({"_id": ObjectId(entry_id)})

    if not entry or entry["user_id"] != session["user_id"]:
        return {"success": False, "error": "Entry not found or unauthorized."}, 403

    new_fav_status = not entry.get("isFavorite", False)

    mongo.db.journal_entries.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": {"isFavorite": new_fav_status}}
    )

    return jsonify({"success": True, "isFavorite": new_fav_status})