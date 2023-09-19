import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        user_id = session["user_id"]
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as totalshares, price FROM transactions WHERE user_id = ? GROUP BY symbol",
            user_id,
        )
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        total = cash

        for stock in stocks:
            total += stock["price"] * stock["totalshares"]

        return render_template(
            "index.html", stocks=stocks, cash=cash, total=total, usd=usd
        )
