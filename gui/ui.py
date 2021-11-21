from datetime import datetime
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from domain.User import User
from controller.UserService import UserService
from domain.enums.ConditionEnum import Condition
from repository.UserRepository import UserRepository
from domain.validator.UserValidator import UserValidator
from datetime import date

Window.size = (300,500)
sportFinished = False
user = "caine"
validator = UserValidator()
repository = UserRepository("localhost", "BEMM")
service = UserService(repository,validator)

class FirstWindow(Screen):
    def afis(self):
        print('caine')

class LoginWindow(Screen):
    def logIn(self):
        global user
        username = self.ids.LoginUsername.text
        user = service.find_one_by_username(username)

class ProfileWindow(Screen):
    def on_enter(self):
        global user
        username = user.get_username()
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        gender = user.get_gender()
        height = user.get_height()
        weight = user.get_weight()
        condition = user.get_condition()
        self.ids.usernameField.text = username
        self.ids.firstNameField.text = firstname
        self.ids.lastNameField.text = lastname
        self.ids.genderField.text = str(gender)
        self.ids.heightField.text = str(height)
        self.ids.weightField.text = str(weight)
        self.ids.conditionField.text = str(condition)
        

class RegisterWindow(Screen):
    def register(self):
        global user
        username = str(self.ids.username.text)
        firstname = str(self.ids.firstname.text)
        lastname = str(self.ids.lastname.text)
        print(username,firstname,lastname)
        user = User(username,firstname,lastname,"F",date.today(),50,210)
        service.save(username,firstname,lastname,"F",date.today(),50,210)


class MainWindow(Screen):
    def on_enter(self):
        completedGoals = 1
        global user
        if service.achieved_sport_habit(user.get_user_id()):
            completedGoals+=1
        if service.achieved_water_habit(user.get_user_id()):
            completedGoals+=1
        user = service.find_one_by_username(user.get_username())
        self.ids.mainLabelNr.text = str(user.get_water_habit().get_number_of_glasses_drunk())
        self.ids.mainLabelTotal.text = str(user.get_water_habit().get_number_of_glasses())
        self.ids.emojiId.source = "gui/static/emoji"+str(completedGoals)+".png"
        self.ids.statusId.source = "gui/static/status"+str(completedGoals)+".png"
    def addWater(self):
        global user
        user = service.find_one_by_username(user.get_username())
        glasses = int(self.ids.mainLabelNr.text)
        glasses += 1
        print("id: ", user.get_user_id(), "glasses: ", glasses)
        service.add_glasses(user.get_user_id())
        self.ids.mainLabelNr.text = str(glasses)


class SleepingWindow(Screen):
    def on_enter(self):
        self.ids.goToSleep.text = str("")
        self.ids.wakeUp.text = str("")

    def when_wake_up(self):
        global user
        hour = int(self.ids.hourToGoToSleep.text)
        minute = int(self.ids.minuteToGoToSleep.text)
        wake_up = service.calculate_when_to_wake_up(user.get_user_id(), (hour, minute))
        self.ids.wakeUp.text = str(str(wake_up[0]) + ":" + str(wake_up[1]))

    def when_go_to_sleep(self):
        global user
        hour = int(self.ids.hourToWakeUp.text)
        minute = int(self.ids.minuteToWakeUp.text)
        go_to_sleep = service.calculate_when_to_go_to_sleep(user.get_user_id(), (hour, minute))
        self.ids.goToSleep.text = str(str(go_to_sleep[0]) + ":" + str(go_to_sleep[1]))

class SportWindow(Screen):
    def on_enter(self):
        global user
        workout =  user.get_sporting_habit().get_actual_workout()
        jumps = workout[0]
        squats = workout[1]
        crunches = workout[2]
        pushUps = workout[3]
        self.ids.actual_jumping_jacks.text = str(jumps)
        self.ids.actual_squats.text = str(squats)
        self.ids.actual_crunches.text = str(crunches)
        self.ids.actual_push_ups.text = str(pushUps)

        workout =  user.get_sporting_habit().get_workout()
        jumps = workout[0]
        squats = workout[1]
        crunches = workout[2]
        pushUps = workout[3]
        self.ids.to_do_jumping_jacks.text = str(jumps)
        self.ids.to_do_squats.text = str(squats)
        self.ids.to_do_crunches.text = str(crunches)
        self.ids.to_do_push_ups.text = str(pushUps)

    def addJumps(self):
        global user
        jumps = int(self.ids.actual_jumping_jacks.text)
        additionalJumps = int(self.ids.nr_jumping_jacks.text)
        self.ids.actual_jumping_jacks.text = str(jumps+additionalJumps)
        service.add_jumping_jacks(user.get_user_id(),additionalJumps)
    
    def addSquats(self):
        global user
        squats = int(self.ids.actual_squats.text)
        additionalSquats = int(self.ids.nr_squats.text)
        self.ids.actual_squats.text = str(squats+additionalSquats)
        service.add_squats(user.get_user_id(),additionalSquats)

    def addCrunches(self):
        global user
        crunches = int(self.ids.actual_crunches.text)
        additionalCrunches = int(self.ids.nr_crunches.text)
        self.ids.actual_crunches.text = str(crunches + additionalCrunches)
        service.add_crunches(user.get_user_id(), additionalCrunches)

    def addPushUps(self):
        global user
        pushUps = int(self.ids.actual_push_ups.text)
        additionalPushUps = int(self.ids.nr_push_ups.text)
        self.ids.actual_push_ups.text = str(pushUps + additionalPushUps)
        service.add_push_ups(user.get_user_id(), additionalPushUps)


class RunWindow(Screen):
    pass

class WindowManager(ScreenManager):     
    pass


kv = Builder.load_file('gui/windows.kv')

class MyApp(App):
    def build(self):
        return kv
