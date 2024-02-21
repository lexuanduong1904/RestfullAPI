from flask import Blueprint, jsonify, request, render_template, url_for, redirect, session, flash
from .service import (sign_up_service, login_service, change_password_service, get_information_user_service, delete_account_service)
import json
users = Blueprint("users", __name__)


@users.route("/home", methods = ['GET'])
def home():
    if "current_admin" in session:
        session.pop("current_admin", None)
    return render_template("home.html")

@users.route("/users/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emailLogin = request.form.get("email", False)
        passwordLogin = request.form.get("password")
        session.permanent = True
        if emailLogin and passwordLogin:
            user_login = login_service(emailLogin, passwordLogin)
            if user_login == None:
                flash("Email or password is invalid", "info")
            else:
                session["current_user"] = user_login
                flash("You logged in successful", "info")
                return redirect(url_for("users.get_information_user", id = user_login["_id"]))
        else:
            flash("Email and password are required fields", "info")
            return render_template("login.html")
    if "current_user" in session:
        user_login = session["current_user"]
        return redirect(url_for("users.get_information_user", id = user_login["_id"]))
    return render_template("login.html")

@users.route("/users/id=<int:id>", methods = ['GET'])
def get_information_user(id):
    if "current_user" in session:
        if (id == session["current_user"]["_id"]):
            current_user = get_information_user_service(id)
            if current_user == None:
                flash("User ID is not used", "info")
            return render_template("user.html", id = current_user["_id"], name = current_user["name"],
                                phone_number = current_user["phone number"], email = current_user["email"])
        else:
            flash("You are not admin", "info")
            return redirect(url_for("users.home"))
    else:
        flash("You must login", "info")
        return redirect(url_for("users.login"))

@users.route("/users/signup", methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        emailSignUp = request.form.get("email", False)
        passwordSignUp = request.form.get("password", False)
        nameSignUp = request.form.get("name", False)
        phone_numberSignUp = request.form.get("phone_number")
        if emailSignUp and passwordSignUp and nameSignUp and phone_numberSignUp:
            new_user = sign_up_service(emailSignUp, passwordSignUp, 
                                       nameSignUp, phone_numberSignUp)
            if new_user == None:
                flash("Email is used", "info")
            else:
                flash("You signed up successful", "info")
        else:
            flash("Email, password, name and phone_number are required fields", "info")
            return render_template("signup.html")
    if "current_user" in session:
        flash("You must logout to create new account", "info")
        return redirect(url_for("users.get_information_user", id = session["current_user"]["_id"]))
    return render_template("signup.html")

@users.route("/users/change_password", methods = ['GET', 'PUT'])
def change_password():
    if "current_user" not in session:
        flash("You are not logged in", "info")
        return redirect(url_for("users.login"))
    else:
        if request.method == 'PUT':
            req = request.get_json()
            if "current_password" not in req or "new_password" not in req:
                flash("Current and New Password are required fields", "info"), 400
            else:
                if req["current_password"] == session["current_user"]["password"]:
                    current_user = session["current_user"]
                    current_user["password"] = req["new_password"]
                    change_password_service(current_user)
                    return redirect(url_for("users.log_out")), 200
                else:
                    flash("Current password is invalid", "info")
                    return render_template("changePassword.html"), 400
        return render_template("changePassword.html")

@users.route("/users/logout", methods = ['GET'])
def log_out():
    if "current_user" in session:
        flash("You logged out", "info")
        session.pop("current_user", None)
    else:
        flash("You are not logged in!", "info")
    return redirect(url_for("users.login"))

@users.route("/users/delete_account", methods=['GET', 'DELETE'])
def delete_account():
    if "current_user" not in session:
        flash("You must login", "info")
        return redirect(url_for("users.login"))
    else:
        if request.method == 'DELETE':
            req = request.get_json()
            if "current_password" not in req:
                return jsonify({"error": "Password is required"}), 400
            if req["current_password"] == session["current_user"]["password"]:
                if delete_account_service(session["current_user"]) == 1:
                    return redirect(url_for("users.log_out")), 200
                return jsonify({"message": "No"}), 400
    return render_template("deleteAccount.html")
