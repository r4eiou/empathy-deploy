from app import create_app
import os
print("Working directory:", os.getcwd())
print("Templates folder exists?", os.path.exists("templates/index.html"))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
