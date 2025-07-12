from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import mongo, bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    """Login page (GET only)"""
    return render_template("index.html", page="login", form_errors={})

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login form submission"""

    # TEMPORARY BYPASS - REMOVE WHEN MONGODB IS FIXED
    BYPASS_AUTH = True  # Set to False when you want normal auth
    
    if BYPASS_AUTH:
        email = request.form.get("email", "").strip()
        if email:
            session["user_id"] = "507f1f77bcf86cd799439011"  # Dummy user ID
            session["user_name"] = "Test User"
            session["user_email"] = email
            flash("Logged in successfully (bypass mode).", "success")
            return redirect(url_for("dashboard.dashboard"))
        

    form_errors = {}
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    # Validate fields
    if not email:
        form_errors["email"] = "Email is required."
    if not password:
        form_errors["password"] = "Password is required."

    if form_errors:
        return render_template("index.html", form_errors=form_errors, request=request, page="login")

    
    print("[DEBUG] mongo =", mongo)
    print("[DEBUG] mongo.db =", mongo.db)

    if mongo.db is None:
        flash("Database connection error.", "error")
        return render_template("index.html", form_errors=form_errors, request=request, page="login")

    # DEBUG: Show all users in the DB
    print("[DEBUG] Users in DB:")
    for u in mongo.db.users.find():
        print(f"• {u.get('email')} - {u.get('full_name')}")

    print(f"[DEBUG] Input Email: '{email}'")


    # Check if user exists
    user = mongo.db.users.find_one({"email": email})
    print(f"[DEBUG] User found: {user}")
    if not user:
        form_errors["email"] = "No account found with this email."
        return render_template("index.html", form_errors=form_errors, request=request, page="login")

    # Check password
    if not bcrypt.check_password_hash(user["password"], password):
        form_errors["password"] = "Incorrect password."
        return render_template("index.html", form_errors=form_errors, request=request, page="login")

    # Successful login
    session["user_id"] = str(user["_id"])
    session["user_name"] = user["full_name"]
    session["user_email"] = user["email"]
    flash("Logged in successfully.", "success")
    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Registration page (GET + POST)"""
    form_errors = {}

    if request.method == "POST":
        full_name = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validate inputs
        if not full_name:
            form_errors["fullname"] = "Full name is required."
        if not email:
            form_errors["email"] = "Email is required."
        if len(password) < 8:
            form_errors["password"] = "Password must be at least 8 characters."

        # Check if email is already registered
        if mongo.db.users.find_one({"email": email}):
            form_errors["email"] = "Email already exists."

        if form_errors:
            return render_template("register.html", form_errors=form_errors, request=request, page="register")

        # Save new user
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        mongo.db.users.insert_one({
            "full_name": full_name,
            "email": email,
            "password": hashed_pw
        })

        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.index"))

    return render_template("register.html", page="register", form_errors={})


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.index"))