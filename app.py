from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "atslega"

def izveidot_db():
    conn = sqlite3.connect("datubaze.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "users"(
    "id"     INTEGER,
    "username"  TEXT,
    "password"  TEXT,
    PRIMARY KEY("id")
    )
    """)
    conn.commit()
    conn.close()
izveidot_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/registreties", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #print(username)
        #print(password) 
  
        conn = sqlite3.connect("datubaze.db")
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO users (username, password) VALUES (?,?) """,(username, password))
        conn.commit()
        conn.close()

        return redirect("/login")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("datubaze.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users WHERE username=? AND password=?""",(username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/filmas")
        else:
            return "Nepareizs lietotājvārds vai parole"
    
    return render_template("login.html")

def filmas_db():

    conn = sqlite3.connect("filmas.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS filmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nosaukums TEXT,
        zanrs TEXT,
        gads INTEGER
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

filmas_db()

@app.route("/filmas", methods=["GET", "POST"])
def filmas():

    conn = sqlite3.connect("filmas.db")
    cursor = conn.cursor()
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("filmas.db")
    cursor = conn.cursor()

    user_id = session["user_id"]


    if request.method == "POST":

        nosaukums = request.form["nosaukums"]
        zanrs = request.form["zanrs"]
        gads = request.form["gads"]

        cursor.execute("""
        INSERT INTO filmas
        (nosaukums, zanrs, gads, user_id)
        VALUES (?, ?, ?, ?)
        """, (nosaukums, zanrs, gads, user_id))


        conn.commit()

    cursor.execute("""
    SELECT * FROM filmas
    WHERE user_id=?
    """, (user_id,))

    filmas = cursor.fetchall()
    conn.commit()
    conn.close()

    return render_template("filmas.html", filmas=filmas)



        


if __name__ == "__main__":
    izveidot_db()
    app.run(debug=True)
