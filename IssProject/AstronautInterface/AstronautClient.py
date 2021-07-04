from datetime import datetime, time
from time import sleep

from AstronautInterface.ResourceUsage import ResourcesState
from Backend.DataStore.CreateTables import dropAllTables, createTables
from Backend.Schedular import Schedular
from CommandLineControler import Controller, NextState
import Backend.ServerAPI as ServerAPI
from GroundControlInterface.Workouts import *

class LoginState:
    def run(self):
        print("--Welcome Astronaut--")
        print("Type 'back' at anytime to return to the previous state")

        usersEmail = None
        loggedIn = False
        while loggedIn != True:
            while usersEmail == None:
                email = input("What is your astronaut login: ")
                if email == "back":
                    return None
                userFound = ServerAPI.doesAstronautWithEmailExist(email)
                if userFound != True:
                    print("An astronaut with that login does not exist")
                else:
                    usersEmail = email

            correctPassword = False
            while correctPassword != True:
                password = input("What is your password: ")
                if password == "back":
                    return None
                correctPassword = ServerAPI.doesUsersPasswordMatch(usersEmail,password)
                if correctPassword != True:
                    print("Incorrect password")
                else:
                    loggedIn = True
            """
            correctMFA = False
            while correctMFA != True:
                mfaCode = input("What is your mfa code: ")
                if mfaCode == "back":
                    return None
                #try:
                correctMFA = ServerAPI.doesUsersMfaCodeMatch(usersEmail, mfaCode.replace(" ", ""))
                if correctMFA != True:
                    print("Incorrect mfa")
                else:
                    loggedIn = True
                #except :
                print('invalid mfa')
                return None
            """

        return NextState(HomeState(usersEmail),False)

class HomeState:
    def __init__(self,email):
        self.email = email

    def run(self):
        print("--Astronaut Home--")
        while True:
            passed = False
            while not passed:
                cmd = input("type 'food', 'workout': ")
                if cmd == 'back':
                    return None
                elif cmd =='food':
                    return NextState(ResourcesState(),False)
                elif cmd =='workout':
                    return NextState(WorkState(self.email), False)
                else:
                    print("invalid input")


class WorkState:
    def __init__(self, email):
        self.email = email

    def countdown(self, t):

        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print( '\r', timer, end='')
            sleep(1)
            t -= 1
        print('\nExercise completed!!')

    def run(self):

        print("--Physical Workout--")
        typeSelected = None
        height = input('What is your height:\n-->')
        weight = input('What is your weight: \n-->')
        time = datetime.now()

        while typeSelected != True:
            cmd = input('Please select\n1. manuel workout selection\n2. automatic assigned workout\n--> ')
            if cmd == "back":
                return None

            if cmd == "1":
                while True:
                    optionEx = input("Select the workout for today (enter stop to end):   ")
                    if optionEx == "1":
                        print(ex1["title"] + ":" + str(ex1["time"]) + " minutes")
                        print("Timer: ")
                        self.countdown(ex1["time"]//10)
                    elif optionEx == "2":
                        print(ex2["title"] + ":" + str(ex2["time"]) + " minutes")
                        print("Timer: ")
                        self.countdown(ex2["time"] // 10)
                    elif optionEx == "3":
                        print(ex3["title"] + ":" + str(ex3["time"]) + " minutes")
                        print("Timer: ")
                        self.countdown(ex3["time"] // 10)
                    elif optionEx == "stop":

                        #ServerAPI.createWorkout(height, weight, str(time), self.email)
                        break

            if cmd == "2":
                print("Your work out is going to be: " + currentWorkout)
                input("Press Enter to get started.")

                for ex in exs:
                    # ex = wk.exs
                    print(ex["title"] + ":" + str(ex["time"]) + " minutes")
                    print("Timer: ")
                    self.countdown(ex["time"] // 10)
                    # for e in ex:
                    #     print(e) #Implement a count down here
                    print("======")
                print("Well done!!!")
                #ServerAPI.createWorkout(height, weight, str(time), self.email)

            typeSelected = True


#dropAllTables()
#createTables()

Schedular.unpause()
controller = Controller()
controller.start(NextState(LoginState(),False))
Schedular.endAllSchedules()