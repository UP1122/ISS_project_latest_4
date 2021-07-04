import json
import pickle
import requests
from Backend.Accounts import addUserAccount, isCorrectPassword, UserAccounts
from Backend.DataStore.AccessLayer import ASTRONAUT, GROUND_CONTROL
from Backend.ISS import getStatesOfShuttles, getIssOxogenLevel, \
    getAstronauts, launchShuttleToAppropriateDestination
from ApiMode import ApiSetting
from Backend.MultiFactorAuthentication import verifyMfaAccount, registerMfaAccount
from Backend.Resources import Resources

def unpickle(text):
    formated = text[1:-2].replace('\\n','\n')
    return pickle.loads(formated.encode())

class IssState:
    def __init__(self,oxogenLevel):
        self.oxogenLevel = oxogenLevel

class AstronautState:
    def __init__(self,email,location,id):
        self.email = email
        self.location = location
        self.id = id

def getResourceQuantity(itemNumber):
    if ApiSetting.distrubuted:
        return int(requests.get("http://127.0.0.1:5000/ResourceItem/"+str(itemNumber)).text)
    else:
        return Resources.getItemStockQuantity(itemNumber)

def consumeResource(itemNumber,amountToConsume):
    if ApiSetting.distrubuted:
        return requests.put("http://127.0.0.1:5000/ResourceItem/"+str(itemNumber) ,params ={"amountToConsume":str(amountToConsume)})
    else:
        return Resources.consumeItemStock(itemNumber,amountToConsume)

def getAvailibleItems():
    if ApiSetting.distrubuted:
        return unpickle(requests.get("http://127.0.0.1:5000/ResourceItems/").text)
    else:
        return Resources.getAllStockedItems()

def getIssState():
    if ApiSetting.distrubuted:
        return unpickle(requests.get("http://127.0.0.1:5000/Iss/").text)
    else:
        return IssState(getIssOxogenLevel())

def getShuttlesStates():
    if ApiSetting.distrubuted:
        return unpickle(requests.get("http://127.0.0.1:5000/Shuttles/").text)
    else:
        return getStatesOfShuttles()

"""
def queryIsAShuttleOnEarth(shuttleNumber):
    if ApiSetting.serverMode:
        return unpickle(requests.get("http://127.0.0.1:5000/ShuttlesLocation/"+str(shuttleNumber)).text)
    else:
        return isShuttleOnEarth(shuttleNumber)
"""

def launchShuttle(shuttleNo, astronautIds):
    if ApiSetting.distrubuted:
        requests.post("http://127.0.0.1:5000/ShuttlesLocation/" + str(shuttleNo),params ={"astronautIds":json.dumps(astronautIds)})
    else:
        launchShuttleToAppropriateDestination(shuttleNo,astronautIds)

def getAstronautsOverview():
    def formatAsStates(astronauts):
        states = []
        for astronaut in astronauts:
            states.append(AstronautState(astronaut.account.email, astronaut.getLocation(), astronaut.id))
        return states

    if ApiSetting.distrubuted:
        return formatAsStates(unpickle(requests.get("http://127.0.0.1:5000/Astronauts/").text))
    else:
        return formatAsStates(getAstronauts())

def doesAstronautWithEmailExist(email):
    return _doesUserOfTypeExist(email,ASTRONAUT)

def doesGroundControlUserWithEmailExist(email):
    return _doesUserOfTypeExist(email,GROUND_CONTROL)

def _doesUserOfTypeExist(email, type):
    if email == 'admin':
        return True
    else:
        user = None
        if ApiSetting.distrubuted:
            user = unpickle(requests.get("http://127.0.0.1:5000/User/", params={"email": email}).text)
        else:
            user = UserAccounts().getUserAccountByEmail(email)

        if user != None and user.accountType == str(type):
            return True
        return False

def doesUsersPasswordMatch(username, password):
        if username == 'admin':
            if password == 'password':
                return True
        else:
            if ApiSetting.distrubuted:
                return unpickle(requests.get("http://127.0.0.1:5000/Password/", params={"email": username,"password":password}).text)
            else:
                return isCorrectPassword(username,password)

def registerUserMfaAccount(email, phone, countryCode):
    if ApiSetting.distrubuted:
        requests.post("http://127.0.0.1:5000/MFA/", params={"email": email,"phone":phone,"countryCode":countryCode})
    else:
        registerMfaAccount(email, phone, countryCode)

def doesUsersMfaCodeMatch(email, mfaCode):
    if ApiSetting.distrubuted:
        return unpickle(requests.get("http://127.0.0.1:5000/MFA/", params={"email": email,"mfaCode":mfaCode}))
    else:
        return verifyMfaAccount(email,mfaCode)

def registerGroundControlEmail(address):
    if ApiSetting.distrubuted:
        requests.post("http://127.0.0.1:5000/User/", params={"email": address,"type":GROUND_CONTROL})
    else:
        addUserAccount(address,GROUND_CONTROL)

def registerAstronautsEmail(address):
    if ApiSetting.distrubuted:
        code = requests.post("http://127.0.0.1:5000/User/", params={"email": address,"type":ASTRONAUT}).status_code
        if code == 501:
            raise Exception("could not create account")
    else:
        addUserAccount(address,ASTRONAUT)

"""
def createWorkout(height, weight, time, user_id):
    if ApiSetting.serverMode:
        raise Exception()#return requests.post("http://127.0.0.1:5000/system/")
    else:
        DataStore.AccessLayer.addWorkout(height, weight, time, user_id)
"""