import pymongo

myDB = pymongo.MongoClient("mongodb://localhost:27017/")
db = myDB["database"]

# Đăng nhập
def login_service(emailLogin, passwordLogin):
    login_user = {"email": emailLogin, "password": passwordLogin}
    data_users = db["users"]
    try:
        user = data_users.find(login_user)[0]
        return user
    except IndexError:
        return None
    
#Hiển thị thông tin người dùng đang đăng nhập
def get_information_user_service(id):
    data_users = db["users"]
    try:
        current_user = data_users.find({"_id": id})[0]
        return current_user
    except IndexError:
        return None

#Đăng ký
def sign_up_service(emailSignUp, passwordSignUp, nameSignUp, phone_numberSignUp):
    data_users = db["users"]
    try:
        used_user = data_users.find({"email": emailSignUp})[0]
        return None
    except IndexError:
        id = data_users.count_documents({})+1
        while data_users.find_one({"_id": id}):
            id += 1
        new_user = {"_id": id, "name": nameSignUp, "phone number": phone_numberSignUp,
                               "email": emailSignUp, "password": passwordSignUp}
        data_users.insert_one(new_user)
        return new_user
    
#Đổi mật khẩu
def change_password_service(current_user):
    data_users = db["users"]
    requestChange = {"email": current_user["email"]}
    newValue = {"$set": {"password": current_user["password"]}}
    data_users.update_one(requestChange, newValue)
    
#Xóa tài khoản
def delete_account_service(current_user):
    data_users = db["users"]
    result = data_users.delete_one(current_user)
    return result.deleted_count
    
    


