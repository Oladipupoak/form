from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS items
                          (id INTEGER PRIMARY KEY,
                           name TEXT,
                           description TEXT);""")
    connection.close()

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    description = request.form["description"]
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)",
                       (name, description))
    connection.close()
    return redirect(url_for("index"))

@app.route("/items")
def items():
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items")
        items_list = cursor.fetchall()
    connection.close()
    return render_template("items.html", items=items_list)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
