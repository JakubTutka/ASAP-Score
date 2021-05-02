from tkinter import Label

import kivy
import mysql.connector

kivy.require("1.9.1")
from kivy.config import Config
Config.set('graphics', 'width', '515')
Config.set('graphics', 'height', '750')
Config.set('graphics', 'resizable', False)

from connected import Connected

from logic.validate_data import Validate
from mysql_files.mysql_app import mysql_users
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class Connected(Widget):
    pass

class MainApp(MDApp):
    isException = None
    my_dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('login.kv')

    def logger(self):
        # self.root.ids.welcome_label.text = f'Witaj {self.root.ids.user.text}!'
        username = self.root.ids.user.text
        password = self.root.ids.password.text

        if self.is_login_fields_no_empty() is False:
            self.show_dialog(error="FIELDS")

        elif mysql_users().is_user_exist(username) is False or mysql_users().is_password_correct(username=username, password=password) is False:
            self.show_dialog(error="WRONG_INPUT")

        elif(self.is_login_fields_no_empty() & mysql_users().is_user_exist(username=username) & mysql_users().is_password_correct(username=username, password=password)):
            self.root.transition.direction = "left"
            self.root.current = "connected_screen"


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

    def show_integrity_error(self):
        pass

    def register(self):
        try:
            mysql_users().register(username=self.root.ids.user_login_label.text, password=self.root.ids.rejestracja_password.text, email=self.root.ids.user_email_label.text)
        except mysql.connector.IntegrityError as err:
            self.isException = True
            self.show_dialog(error="ACCOUNT")

    def validate(self):
        is_password_correct = Validate().checkPassword(self.root.ids.rejestracja_password.text)
        is_email_correct = Validate().checkEmail(self.root.ids.user_email_label.text)

        if (self.is_register_fields_no_empty() & is_password_correct & is_email_correct & self.is_password_equals()):
            self.register()
            if not self.isException:
                self.root.transition.direction = 'left'
                self.root.current = "screen3"
                self.clearRegistration()
        else:
            self.show_dialog(error="FIELDS")

    def show_dialog(self, error):
        if(error == "FIELDS"):
            my_dialog = MDDialog(text="Źle wprowadzone dane!")
            my_dialog.open()
        elif (error == "ACCOUNT"):
            my_dialog = MDDialog(text="Istnieje już użytkownik o jednym z wprowadzonych parametrów.")
            my_dialog.open()
        elif (error == "WRONG_INPUT"):
            my_dialog = MDDialog(text="Wprowadzone dane są złe. Spróbuj ponownie.")
            my_dialog.open()

    def is_password_equals(self):
        if (self.root.ids.rejestracja_password.text == self.root.ids.rejestracja_password_retype.text):
            return True
        else:
            return False

    def is_register_fields_no_empty(self):
        if (bool(self.root.ids.user_login_label.text) & bool(self.root.ids.user_email_label.text) & bool(self.root.ids.rejestracja_password.text) & bool(self.root.ids.rejestracja_password_retype.text)):
            return True
        else:
            return False

    def is_login_fields_no_empty(self):
        if (bool(self.root.ids.user.text) & bool(self.root.ids.password.text)):
            return True
        else:
            return False

MainApp().run()