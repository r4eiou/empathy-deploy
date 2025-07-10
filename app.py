from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Scss(app)  

# http://127.0.0.1:5000/
@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
