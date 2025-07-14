from flask import Blueprint, session, redirect, url_for, render_template, request, flash

dash_bp = Blueprint("dashboard", __name__)

@dash_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))


    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        date = request.form.get("password", "")

        # Validate inputs
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title and content:
            # TODO: Save new journal entry

            flash("Entry created successfully!", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Please fill in all fields", "error")
    
    return render_template("dashboard.html")
