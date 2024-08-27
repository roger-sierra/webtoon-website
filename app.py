from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL configurations using environment variables
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rate", methods=["GET", "POST"])
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
