from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, flash
from flask_login import current_user, login_user, login_required, logout_user
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from extras import error, usd, login_required
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.jinja_env.filters["usd"] = usd

db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


TRANSACTIONS = [
    "Deposit",
    "Withdrawal"
]
TYPES = [
    "Checking",
    "Saving"
]

# Main body of the application begins here
# Define data to be set in the index or home page of the application
@app.route("/")
@login_required
def index():
    user = session["user"]
    accounts = db.execute("SELECT account, SUM(amount) as amounts, type, time FROM accounts WHERE user_id = ? GROUP BY account", user)
    username = db.execute("SELECT user FROM users WHERE id = ?", user)[0]["user"]
    return render_template("index.html", accounts=accounts, usd=usd, username=username)

# Create a login page that requires a unique user login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return error("Please enter an email", 403)

        password = request.form.get("password")
        if not password:
            return error("please enter a password", 403)

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return apology("invalid username and/or password", 403)

        user = session["user"] = rows[0]["id"]
        db.execute("INSERT INTO account_type (user_id, account_type) VALUES (?, ?)", user, "Checking")
        db.execute("INSERT INTO account_type (user_id, account_type) VALUES (?, ?)", user, "Saving")
        return redirect("/")

    else:
        return render_template("login.html")

# Create a registration page for new users
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return error("Please input username", 400)

        email = request.form.get("email")
        if not email:
            return error("Please input email", 400)

        password = request.form.get("password")
        if not password:
            return error("Please input password", 400)

        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (user, email, password) VALUES (?, ?, ?)", username, email, hash)
            return redirect("/")
        except:
            return error("Username has already been taken", 400)

    else:
        return render_template("register.html")

# Log existing user out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Create a page where users can update their accounts with new balances
@app.route("/update", methods=["POST", "GET"])
@login_required
def update():
    user = session["user"]
    if request.method == "POST":

        amount = float(request.form.get("amount"))
        if not amount:
            return error("Please enter an amount", 400)

        transaction = request.form.get("transaction")
        if not transaction:
            return error("Please enter a type of transaction", 400)
        if transaction not in TRANSACTIONS:
            return error("Please select a valid type", 403)

        description = request.form.get("description")
        if not description:
            return error("Please enter a description", 400)

        account = request.form.get("account")
        if not account:
            return error("Please enter an account", 400)

        else:
            if transaction == "Withdrawal":
                amount = -amount
                sum = db.execute("SELECT SUM(amount) FROM accounts WHERE account = ?", account)[0]["SUM(amount)"]
                if amount + sum <= 0:
                    return error("Not enough funds", 400)
            else:
                amount = amount

            db.execute("INSERT INTO accounts (user_id, account, amount, type, descrip) VALUES (?, ?, ?, ?, ?)",
                        user, account, amount, transaction, description)
            return redirect("/")

    else:
        type_of_account = db.execute("SELECT account_type FROM account_type WHERE user_id = ? GROUP BY account_type", user)
        return render_template("update.html", transactions=TRANSACTIONS, type_of_account=type_of_account)

@app.route("/history")
@login_required
def history():
    user = session["user"]
    history = db.execute("SELECT * FROM accounts WHERE user_id = ?", user)
    return render_template("history.html", history=history, usd=usd)


# Create a page to help the user transfer money from account to account
@app.route("/transfer", methods=["POST", "GET"])
@login_required
def transfer():
    user = session["user"]
    if request.method == "POST":
        account_from = request.form.get("transfer_from")
        if not account_from:
            return error("Please select an account", 404)

        account_to = request.form.get("transfer_to")
        if not account_to:
            return error("Please select an account", 404)
        if account_to == account_from:
            return error("Accounts must be different", 404)
        amount = float(request.form.get("amount"))

        # Transfer and update accounts
        cash_from = db.execute("SELECT SUM(amount) FROM accounts WHERE user_id = ? AND account = ?",
                                user, account_from)[0]["SUM(amount)"]
        if cash_from < amount:
            return error("Not enough cash to transfer", 404)

        db.execute("INSERT INTO accounts (user_id, account, amount, type, descrip) VALUES (?, ?, ?, ?, ?)",
                    user, account_from, -amount, "Transfer from", "Transfer from")
        db.execute("INSERT INTO accounts (user_id, account, amount, type, descrip) VALUES (?, ?, ?, ?, ?)",
                    user, account_to, amount, "Transfer to", "Transfer to")
        return redirect("/")
    else:
        type_of_account = db.execute("SELECT account_type FROM account_type WHERE user_id = ? GROUP BY account_type", user)
        return render_template("transfer.html", accounts=type_of_account)

# Allow user to create a new account of their own naming
@app.route("/new_account", methods=["GET", "POST"])
@login_required
def new_account():
    user = session["user"]
    if request.method == "POST":
        account_type = request.form.get("account_type")
        if not account_type:
            return error("Please select account type", 400)

        account_name = request.form.get("account_name")
        if not account_name:
            return error("Please name your new account", 400)

        db.execute("INSERT INTO accounts (user_id, account, amount, type, descrip, name) VALUES (?, ?, ?, ?, ?, ?)",
                    user, account_name, "0", "account creation", "-", account_type)
        db.execute("INSERT INTO account_type (user_id, account_type) VALUES (?, ?)", user, account_name)

        return redirect("/")

    else:
        return render_template("new_account.html", types=TYPES)

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    user = session["user"]
    if request.method == "POST":
        account = request.form.get("account")
        if not account:
            return error("Please enter an account", 400)
        sum = db.execute("SELECT SUM(amount) FROM accounts WHERE user_id = ? AND account = ?", user, account)[0]["SUM(amount)"]
        if sum > 0:
            return error("Please transfer funds before closing account", 400)

        db.execute("DELETE FROM accounts WHERE user_id = ? AND account = ?", user, account)
        return redirect("/")

    else:
        type_of_account = db.execute("SELECT account_type FROM account_type WHERE user_id = ? GROUP BY account_type", user)
        return render_template("delete.html", types=type_of_account)