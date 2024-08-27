from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)


@app.route("/create_tables")
def create_table():
    cur = mysql.connection.cursor()

    # Create the webtoons table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS webtoons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        genre VARCHAR(50) NOT NULL,
        description TEXT
        );
    """)

    # Create the ratings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rating INT NOT NULL,
        webtoon_id INT,
        FOREIGN KEY (webtoon_id) REFERENCES webtoons(id)
        );
    """)

    mysql.connection.commit()
    cur.close()
    return "Tables created successfully!"


@app.route("/show_tables")
def show_tables():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES;")
    tables = cur.fetchall()
    return str(tables)


if __name__ == "__main__":
    app.run(debug=True)
