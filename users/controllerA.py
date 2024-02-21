from flask import Blueprint, jsonify, request, flash, url_for, render_template, redirect, session
from .serviceA import (admin_login_service, get_information_admin_service, 
                       admin_change_password_service, add_new_admin_service, 
                       admin_get_information_user_service, delete_admin_account_service, delete_user_service)

admins = Blueprint("admins", __name__)

@admins.route("/admins/home", methods = ['GET'])
def admin_home():
    if "current_user" in session:
        session.pop("current_user", None)
    return render_template("homeAd.html")

@admins.route("/admins/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        emailAdmin = request.form.get("email", False)
        passwordAdmin = request.form.get("password", False)
        session.permanent = True
        if emailAdmin and passwordAdmin:
            admin_login = admin_login_service(emailAdmin, passwordAdmin)
            if admin_login == None:
                flash("Email or password is invalid", "info")
            else:
                session["current_admin"] = admin_login
                flash("You are admin", "info")
                return redirect(url_for("admins.get_information_admin", aid = admin_login["_id"]))
        else:
            flash("Email and password are required fields", "info")
            return render_template("loginAd.html")
    if "current_admin" in session:
        admin_login = session["current_admin"]
        return redirect(url_for("admins.get_information_admin", aid = admin_login["_id"]))
    return render_template("loginAd.html")

@admins.route("/admins/aid=<int:aid>", methods=['GET'])
def get_information_admin(aid):
    if "current_admin" in session:
        if aid == session["current_admin"]["_id"]:
            current_admin = get_information_admin_service(aid)
            if current_admin == None:
                flash("Admin ID is not used", "info")
            return render_template("admin.html", aid = current_admin["_id"], name = current_admin["name"],
                                   phone_number = current_admin["phone number"], email = current_admin["email"])
        else:
            flash("You cannot show information other admin", "info")
            return redirect(url_for("admins.admin_home"))
    else:
        flash("You must login", "info")
        return redirect(url_for("admins.admin_login"))
    
@admins.route("/admins/get_infor_user_id=<int:uid>", methods=['GET'])
def admin_get_information_user(uid):
    if "current_admin" not in session:
        flash("You must login by admin account", "info")
        return redirect(url_for("admins.admin_login"))
    else:
        result = admin_get_information_user_service(uid)
        if result != None:
            return jsonify(result), 200
        else:
            return jsonify(data=None), 400

    
@admins.route("/admins/get_infor_user", methods=['GET'])
def get_info():
    return render_template("adminSearch.html")

@admins.route("/admins/change_password", methods=['GET', 'POST'])
def admin_change_password():
    if "current_admin" not in session:
        flash("You are not logged in", "info")
        return redirect(url_for("admins.admin_login"))
    else:
        if request.method == 'POST':
            new_pass = request.form.get("new_password")
            if new_pass:
                current_admin = session["current_admin"]
                current_admin["password"] = new_pass
                admin_change_password_service(current_admin)
                flash("You have already changed password", "info")
                return redirect(url_for("admins.admin_logout"))
            else:
                flash("New password is required field", "info")
        return render_template("changePasswordAd.html")
    
@admins.route("/admins/add_new_admin", methods=['GET', 'POST'])
def add_new_admin():
    if "current_admin" not in session:
        flash("You must login to add new admin", "info")
        return redirect(url_for("admins.admin_login"))
    if request.method == 'POST':
        newAdminEmail = request.form.get("email", False)
        newAdminPassword = request.form.get("password", False)
        newAdminName = request.form.get("name", False)
        newAdminPhoneNumber = request.form.get("phone_number")
        if newAdminEmail and newAdminPassword and newAdminName and newAdminPhoneNumber:
            new_admin = add_new_admin_service(newAdminEmail, newAdminPassword, newAdminName, newAdminPhoneNumber)
            if new_admin == None:
                flash("Email is used", "info")
            else:
                flash("You added new admin account successful", "info")
        else:
            flash("Email, password, name and phone number are required fields", "info")
            return render_template("addNewAdmin.html")
    return render_template("addNewAdmin.html")

@admins.route("/admins/delete_account", methods=['GET', 'DELETE'])
def delete_admin_account():
    if "current_admin" not in session:
        flash("You must login", "info")
        return redirect(url_for("admins.admin_login"))
    if request.method == 'DELETE':
        req = request.get_json()
        if "current_password" not in req:
            return jsonify({"error": "Password is required"}), 400
        if req["current_password"] == session["current_admin"]["password"]:
            if delete_admin_account_service(session["current_admin"]) == 1:
                return redirect(url_for("admins.admin_logout")), 200
        else:
            return jsonify({"message": "Password is invalid"}), 400
    return render_template("deleteAccountAdmin.html")

@admins.route("/admins/logout", methods=['GET'])
def admin_logout():
    if "current_admin" in session:
        flash("You have logged out", "info")
        session.pop("current_admin", None)
    else:
        flash("You are not admin", "info")
    return redirect(url_for("admins.admin_login"))

@admins.route("/admins/delete_user_id=<int:uid>", methods=['DELETE'])
def delete_user(uid):
    if "current_admin" not in session:
        flash("You must login", "info")
        return redirect(url_for("admins.admin_login"))
    if delete_user_service(uid) == 1:
        return jsonify({"message": "You already have delete userId:"+str(uid)}), 200
    else:
        return jsonify({"message": "Failed"}), 400