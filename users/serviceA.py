import pymongo

myDB = pymongo.MongoClient("mongodb://localhost:27017/")
db = myDB["database"]

#Admin đăng nhập
def admin_login_service(emailAdmin, passwordAdmin):
    login_admin = {"email": emailAdmin, "password": passwordAdmin}
    data_admins = db["admins"]
    try:
        admin = data_admins.find(login_admin)[0]
        return admin
    except IndexError:
        return None

#Hiển thị thông tin admin
def get_information_admin_service(aid):
    data_admins = db["admins"]
    try:
        current_admin = data_admins.find({"_id": aid})[0]
        return current_admin
    except IndexError:
        return None
    
#Đổi mật khẩu admin
def admin_change_password_service(current_admin):
    data_admins = db["admins"]
    requestChange = {"email": current_admin["email"]}
    newValue = {"$set": {"password": current_admin["password"]}}
    data_admins.update_one(requestChange, newValue)

#Thêm tài khoản admin
def add_new_admin_service(newAdminEmail, newAdminPassword, newAdminName, newAdminPhoneNumber):
    data_admins = db["admins"]
    try:
        used_admin = data_admins.find({"email": newAdminEmail})[0]
        return None
    except IndexError:
        aid = data_admins.count_documents({})+1
        while data_admins.find_one({"_id": aid}):
            aid += 1
        new_admin = {"_id": aid, "name": newAdminName, "phone number": newAdminPhoneNumber,
                     "email": newAdminEmail, "password": newAdminPassword}
        data_admins.insert_one(new_admin)
        return new_admin
    
#Xóa tài khoản admin
def delete_admin_account_service(current_admin):
    data_admins = db["admins"]
    result = data_admins.delete_one(current_admin)
    return result.deleted_count

def admin_get_information_user_service(uid):
    data_users = db["users"]
    if uid != 0:
        try:
            result_user = data_users.find({"_id": uid})[0]
            return result_user
        except IndexError:
            return None
    else:
        result = data_users.find()
        return list(result)
    
def delete_user_service(uid):
    data_users = db["users"]
    result = data_users.delete_one({"_id": uid})
    return result.deleted_count

