from flask import Flask, render_template, request, redirect, session, url_for, flash
import json, os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load users from JSON
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

# Save users to JSON
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        mobile = request.form["mobile"]
        password = request.form["password"]
        users = load_users()
        if mobile in users:
            flash("User already exists")
        else:
            users[mobile] = {"password": password, "wallet": 0}
            save_users(users)
            flash("Signup successful")
            return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form["mobile"]
        password = request.form["password"]
        users = load_users()
        if mobile in users and users[mobile]["password"] == password:
            session["user"] = mobile
            return redirect("/wallet")
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/wallet")
def wallet():
    if "user" not in session:
        return redirect("/login")
    users = load_users()
    user_data = users.get(session["user"], {})
    return render_template("wallet.html", balance=user_data.get("wallet", 0))

@app.route("/deposit")
def deposit():
    return render_template("deposit.html", upi="8143877184@ybl")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["mobile"] == "8143877184" and request.form["password"] == "tharun3544R":
            session["admin"] = True
            return redirect("/admin/dashboard")
        flash("Invalid admin credentials")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")
    users = load_users()
    return render_template("admin_dashboard.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
