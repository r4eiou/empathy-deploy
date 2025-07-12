from flask import Blueprint, render_template, current_app, session, redirect, url_for, flash
from bson import ObjectId 
from app.extensions import mongo

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
def page():
    # Redirect if user is not logged in
    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.index"))

    print("[DEBUG] Looking up user by ID:", session["user_id"])

    user_id = ObjectId(session["user_id"])
    user = mongo.db.users.find_one({"_id": user_id})

    print("[DEBUG] Found user:", user)

    if not user:
        flash("User not found.", "error")
        return redirect(url_for("auth.index"))

    # ASSUMPTION:
    # For development/demo purposes, we assume each user should have a default set of memes.
    # If the 'memes' field is missing or currently empty, we automatically insert a preset list of meme filenames.
    # These image files must exist inside 'static/memes/'.
    #
    # This approach is temporary and designed to help populate UI without a full upload system yet.
    # In production, this logic should be removed or replaced with actual meme creation/upload functionality.
    if "memes" not in user or not user["memes"]:
        default_memes = [
            "meme-1.png",
            "meme-2.png",
            "meme-3.png",
            "meme-4.png"
        ]

        # Update the current user's document in MongoDB with the default memes
        mongo.db.users.update_one(
            {"_id": user_id},
            {"$set": {"memes": default_memes}}
        )

        # Also update the local variable so we pass the updated memes to the template
        user["memes"] = default_memes

        print("[DEBUG] Default memes added to user.")

    # Get the list of memes to pass to the profile.html template
    memes = user["memes"]
    print("[DEBUG] User memes:", memes)

    return render_template("profile.html",
        memes=memes,
        username=user.get("full_name", "Guest"),
        useremail=user.get("email", "anonymous@example.com")
    )
