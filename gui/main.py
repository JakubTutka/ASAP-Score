import pandas as pd
import kivy
import mysql.connector

kivy.require("1.9.1")
from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

from gui.scraping_football import FootballScrap

from logic.validate_data import Validate
from mysql_files.mysql_app import MysqlUsers
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock

class OneLineListItemAligned(OneLineListItem):
    def __init__(self, halign, **kwargs):
        super(OneLineListItemAligned, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = halign


class ConnectedScreen(Screen):

    matches_list = []
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_once(self.create_list)

    def on_pre_enter(self, *args):
        scrap = FootballScrap()
        scrap.create_data_frame(10)
        self.matches_list = scrap.matches_to_list()
        Clock.schedule_once(self.create_list)

    def create_list(self, *args):
        matches_list = self.matches_list
        print("jebać strajk kobiet (pozdrawiam Kamil)" + " " + str(len(matches_list)))
        for i in range(0, len(matches_list)):
            self.ids.list_of_matches.add_widget(OneLineListItemAligned(text=matches_list[i], on_release = self.show_match_dialog, halign='center'))

    def show_match_dialog(self, onelinelistitem):
        my_dialog = MDDialog(text=onelinelistitem.text)
        my_dialog.open()

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

        elif MysqlUsers().is_user_exist(username) is False or MysqlUsers().is_password_correct(username=username,
                                                                                               password=password) is False:
            self.show_dialog(error="WRONG_INPUT")

        elif self.is_login_fields_no_empty() & MysqlUsers().is_user_exist(
                username=username) & MysqlUsers().is_password_correct(username=username, password=password):
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
            MysqlUsers().register(username=self.root.ids.user_login_label.text,
                                  password=self.root.ids.rejestracja_password.text,
                                  email=self.root.ids.user_email_label.text)
        except mysql.connector.IntegrityError as err:
            self.isException = True
            self.show_dialog(error="ACCOUNT")

    def validate(self):
        is_password_correct = Validate().checkPassword(self.root.ids.rejestracja_password.text)
        is_email_correct = Validate().checkEmail(self.root.ids.user_email_label.text)

        if self.is_register_fields_no_empty() & is_password_correct & is_email_correct & self.is_password_equals():
            self.register()
            if not self.isException:
                self.root.transition.direction = 'left'
                self.root.current = "screen3"
                self.clearRegistration()
        else:
            self.show_dialog(error="FIELDS")

    def show_dialog(self, error):
        if error == "FIELDS":
            my_dialog = MDDialog(text="Źle wprowadzone dane!")
            my_dialog.open()
        elif error == "ACCOUNT":
            my_dialog = MDDialog(text="Istnieje już użytkownik o jednym z wprowadzonych parametrów.")
            my_dialog.open()
        elif error == "WRONG_INPUT":
            my_dialog = MDDialog(text="Wprowadzone dane są złe. Spróbuj ponownie.")
            my_dialog.open()

    def is_password_equals(self):
        if self.root.ids.rejestracja_password.text == self.root.ids.rejestracja_password_retype.text:
            return True
        else:
            return False

    def is_register_fields_no_empty(self):
        if (bool(self.root.ids.user_login_label.text) & bool(self.root.ids.user_email_label.text) & bool(
                self.root.ids.rejestracja_password.text) & bool(self.root.ids.rejestracja_password_retype.text)):
            return True
        else:
            return False

    def is_login_fields_no_empty(self):
        if bool(self.root.ids.user.text) & bool(self.root.ids.password.text):
            return True
        else:
            return False


MainApp().run()
