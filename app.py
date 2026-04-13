from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def izveidot_db():
    conn = sqlite3.connect("datubaze.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE "users"(
    "id"  INTEGER,
    "username" TEXT,
    "password" TEXT,
    PRIMARY KEY("id")
    )
    """)
    conn.commit()
    conn.close()
izveidot_db()
