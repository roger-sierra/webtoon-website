from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# MySQL configurations using environment variables
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash the password for security
        password_hash = generate_password_hash(password)

        # Save the user to the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password_hash)"
                    "VALUES (%s, %s, %s);", (username, email, password_hash))
        mysql.connection.commit()
        cur.close()

        flash("Registration successful! You can now log in.",
              "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            # Store user ID in session
            session["user_id"] = user[0]
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate_webtoon():
    if request.method == "POST":
        # Get data from the form
        webtoon_id = request.form.get("webtoon_id")
        rating = request.form.get("rating")

        # Insert rating into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ratings (webtoon_id, rating) VALUES "
                    "(%s, %s);", (webtoon_id, rating))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("rate_webtoon"))

    # Fetch webtoons from the database for the dropdown list
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title FROM webtoons;")
    webtoons = cur.fetchall()
    cur.close()

    return render_template("rate.html", webtoons=webtoons)


if __name__ == "__main__":
    app.run(debug=True)
