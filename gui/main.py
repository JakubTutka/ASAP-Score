from tkinter import Label

import kivy
kivy.require("1.9.1")
from connected import Connected

from mysql_files.mysql_app import mysql_users
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, SlideTransition

class Screen1():
    pass
class Screen2():
    pass
class ScreenManager():
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('login.kv')
    def logger(self):
        self.root.ids.welcome_label.text = f'Witaj {self.root.ids.user.text}!'

    def clear(self):
        self.root.ids.welcome_label.text = "Witaj!"
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""

    def clearRegistration(self):
        self.root.ids.rejestracja_label.text = "Rejestracja!"
        self.root.ids.user_login_label.text = ""
        self.root.ids.user_email_label.text = ""
        self.root.ids.rejestracja_password.text = ""
        self.root.ids.rejestracja_password_retype.text = ""

    def register(self):
        mysql_users().register(username=self.root.ids.user_login_label.text, password=self.root.ids.rejestracja_password.text, email=self.root.ids.user_email_label.text)



MainApp().run()