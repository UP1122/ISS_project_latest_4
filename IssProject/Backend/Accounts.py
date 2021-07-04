from random import randrange
from SendEmail import SendEmailFromProjectAccount
from .DataStore import AccessLayer

class UserAccount:
    def __init__(self,email,id):
        self.email = email
        self.accountType = None
        self.name = 'default name'
        self.id = id

    def setPassword(self,newPasword):
        AccessLayer.setUserPassword(self.email,newPasword)
    def getPassword(self):
        return AccessLayer.getUserByEmail(self.email)[4]

class UserAccounts:
    def addUserAccount(self, email,type):
        if self.getUserAccountByEmail(email) != None:
            raise ValueError()
        AccessLayer.addUser(email, 'DEFAULT_PASSWORD', type)

    def getUserAccountsByType(self,type):
        rows = AccessLayer.getUsers()
        if rows == None:
            return []
        accounts = []
        for row in rows:
            accountType = row[2]
            if accountType == type:
                accounts.append(self._createUserAccountObject(row))
        return accounts

    def getUserAccountByEmail(self, email):
        rows = AccessLayer.getUserByEmail(email)
        if rows == None:
            return None
        return self._createUserAccountObject(rows)

    def getUserAccountById(self, id):
        rows = AccessLayer.getUserById(id)
        if rows == None:
            return None
        return self._createUserAccountObject(rows)

    def _createUserAccountObject(self, rows):
        account = UserAccount(rows[1],rows[0])
        account.accountType = rows[2]
        return account

def addUserAccount(emailAddress,type):
    UserAccounts().addUserAccount(emailAddress,type)
    astronaut = UserAccounts().getUserAccountByEmail(emailAddress)
    randomPassword = generateRandomPassword()
    astronaut.setPassword(randomPassword)
    SendEmailFromProjectAccount(emailAddress, 'Your password is ' + randomPassword)

def generateRandomPassword():
    return str(randrange(1000,9999))

def isCorrectPassword(email,passwordIn):
    user = UserAccounts().getUserAccountByEmail(email)
    password = user.getPassword()
    return password == passwordIn