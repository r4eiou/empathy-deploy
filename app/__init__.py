import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import mongo, bcrypt, sess

def create_app():
    load_dotenv()

    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"
    

    # Initialize extensions with the app instance
    mongo.init_app(app)
    bcrypt.init_app(app)
    sess.init_app(app)

    # Test the connection
    try:
        with app.app_context():
            mongo.cx.server_info() 
            print("✅ MongoDB connected successfully!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

    # Register routes
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dash_bp
    from app.routes.journal import journal_bp
    from app.routes.profile import profile_bp
    from app.routes.allEntries import all_entries_bp
    from app.routes.entry import entry_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(all_entries_bp)
    app.register_blueprint(entry_bp)

    return app
