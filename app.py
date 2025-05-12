from flask import Flask, render_template, request, redirect, session
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'

cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def index():
    if "admin" in session:
        return redirect("/panel")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if email == "admin@mauka.com" and password == "admin123":
        session["admin"] = email
        return redirect("/panel")
    return render_template("login.html", error="Credenciales incorrectas")

@app.route("/panel")
def panel():
    if "admin" not in session:
        return redirect("/")
    return render_template("panel.html")

@app.route("/usuarios")
def usuarios():
    if "admin" not in session:
        return redirect("/")
    users = auth.list_users().users
    return render_template("usuarios.html", users=users)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
