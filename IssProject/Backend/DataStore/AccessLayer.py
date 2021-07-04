from Connection import Connection
from cryptography.fernet import Fernet
from enum import Enum
from Backend.crypt1 import encrypt_message
from Backend.crypt1 import decrypt_message
from Backend.crypt1 import load_key
from Backend import *
import os
import sqlite3


class Location(Enum):
    EARTH = 0,
    FLYING = 1,
    SPACE_STATION = 2


ASTRONAUT = 'ASTRONAUT'
GROUND_CONTROL = 'GROUND_CONTROL'
ADMIN = 'ADMIN'


def getUserByEmail(email):
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id WHERE email ='" + email + "';"
    userRows = Connection.createConnection().execute_query(select_user)
    if len(userRows) == 0:
        print("None")
    else:
        print(userRows)


getUserByEmail(input("email"))

def getUserById(id):
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id WHERE user_id ='" + str(id) + "';"
    userRows = Connection.createConnection().execute_query(select_user)
    if len(userRows) == 0:
        return None
    return userRows[0]


def checkpassword():
    a = input("email")
    select_user_id = "SELECT id FROM users WHERE email ='" + a + "'"
    rows = Connection.createConnection().execute_query(select_user_id)
    usid = (rows[0][0])
    print(usid)
    if usid == 0:
        print("Not found")
    elif usid != 0:
        pl = str(usid)
        print(pl)

        b = input("Password")

        get_password = "SELECT password FROM passwords  WHERE user_id ='" + pl + "'"
        rows2 = Connection.createConnection().execute_query(get_password)
        rows2 = str(rows2)
        rows3 = bytes(rows2, 'utf-8')
        decoded_password = decrypt_message(rows3)
        rows4 = decoded_password.decode('utf-8')
        print(rows4)
        if b == rows4:
            print("Correct password")
        else:
            print("error")


#checkpassword()


def getUsers():
    a = input("password")
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id;"
    userRows = Connection.createConnection().execute_query(select_user)
    if len(userRows) == 0:
        return None
    else:
        if a in userRows:
            print(decrypt_message(a))


def addUser(email, password, userType):
    encrypted_password = encrypt_message(password).decode()
    insert_user = """INSERT INTO users (email,user_type) VALUES (""" + "'" + email + "'," + "'" + userType + "'" + ");"
    id = Connection.createConnection().execute_query(insert_user)
    insert_password = """INSERT INTO passwords (password,user_id) VALUES (""" + "'" + encrypted_password + "'," + str(
        id) + ");"
    if userType == ASTRONAUT:
        groundLocationString = str(Location.EARTH).split('.')[1]
        insert_astronaut_location = """INSERT INTO astronaut_locations (location,user_id) VALUES (""" + "'" + groundLocationString + "'," + str(
            id) + ");"
        Connection.createConnection().execute_query(insert_astronaut_location)

    Connection.createConnection().execute_query(insert_password)
    return id


#addUser("u.parak@live.com","123456","Astronaut")

def setUserPassword(email, password):
    encrypted_password = encrypt_message(password).decode()
    select_user_id = "SELECT id FROM users WHERE email ='" + email + "'"
    rows = Connection.createConnection().execute_query(select_user_id)
    id = rows[0][0]
    update_password = "UPDATE passwords SET password = '" + encrypted_password + "' WHERE user_id = " + str(id) + ";"
    Connection.createConnection().execute_query(update_password)


def storeMfaId(email, mfaId):
    insert_mfa_account = """INSERT INTO mfa_accounts (email,mfa_code) VALUES (""" + "'" + email + "'," + "'" + str(
        mfaId) + "'" + ");"
    Connection.createConnection().execute_query(insert_mfa_account)


def getMfaId(email):
    select_mfa_account = "SELECT mfa_code FROM mfa_accounts WHERE email ='" + email + "'"
    res = Connection.createConnection().execute_query(select_mfa_account)
    return res[0][0]


def getAstronautLocation(email):
    select_location = "SELECT * FROM astronaut_locations JOIN users ON users.id = astronaut_locations.user_id WHERE email ='" + email + "' ;"
    userLocationRows = Connection.createConnection().execute_query(select_location)
    if len(userLocationRows) == 0:
        return None
    return userLocationRows[0][1]


def setAstronautLocation(location, email):
    select_user_id = "SELECT id FROM users WHERE email ='" + email + "'"
    rows = Connection.createConnection().execute_query(select_user_id)
    id = rows[0][0]
    locationString = str(location).split('.')[1]
    update_location = "UPDATE astronaut_locations SET location = '" + locationString + "' WHERE user_id = " + str(
        id) + ";"
    Connection.createConnection().execute_query(update_location)


def getItemStockQuantity(itemNumber):
    select_item_stock_quantity = "SELECT qtyonhand FROM items WHERE itemNumber =" + str(itemNumber) + ";"
    rows = Connection.createConnection().execute_query(select_item_stock_quantity)
    return rows[0][0]


def consumeItemStock(itemNumber, quantity):
    update_item_quantity = "UPDATE items SET qtyonhand = qtyonhand - " + str(quantity) + " WHERE itemNumber  = " + str(
        itemNumber) + ";"
    Connection.createConnection().execute_query(update_item_quantity)


def getAllStockedItems():
    select_item_stock_quantity = "SELECT * FROM items;"
    return Connection.createConnection().execute_query(select_item_stock_quantity)


def addWorkout(height, weight, time, user):
    insert_workout = """INSERT INTO workout (weight,height, workout_time, user)
     VALUES (""" + "'" + weight + "'," + "'" + height + "'," + "'" + time + "'," + "'" + user + "'" + ");"
    id = Connection.createConnection().execute_query(insert_workout)
    return id
