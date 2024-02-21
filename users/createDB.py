import random
from faker import Faker
import pymongo

myData = pymongo.MongoClient("mongodb://localhost:27017/")
db = myData["database"]

users_db = db["users"]

def createDB_users():
    fake = Faker()
    data_users = []
    print("Number of users:", end=" ")
    NumberOfUsers = int(input())
    for id in range(NumberOfUsers):
        user = {"_id": id+1, "name": fake.name(), "phone number": fake.phone_number(),
                "email": fake.email(), "password": str(random.randint(1000000, 9999999))}
        data_users.append(user)
    print("Created DB users")
    return data_users
users_db.insert_many(createDB_users())

admins_db = db["admins"]

def createDB_admins():
    fake = Faker()
    data_admins = []
    print("Number of admins:", end=" ")
    NumberOfAdmins = int(input())
    for id in range(NumberOfAdmins):
        admin = {"_id": id+1, "name": fake.name(), "phone number": fake.phone_number(),
                "email": fake.email(), "password": str(random.randint(1000000, 9999999))}
        data_admins.append(admin)
    print("Created DB admins")
    return data_admins
admins_db.insert_many(createDB_admins())