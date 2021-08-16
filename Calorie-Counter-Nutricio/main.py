from tensorflow import keras
import tensorflow.keras.backend as K
import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
import webbrowser
import threading
import cv2
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from database import DataBase
import seaborn as sns
from matplotlib.ticker import FuncFormatter

screen_helper = """
ScreenManager:
    StartingPage:
    LoginPage:
    SignUpPage:
    HomePage
    ScanPage:
    ReportPage:
    FinalResultPage:
    CalculatorPage:
    CalculatorResultPage:
    SettingPage:
    
<StartingPage>:
    name: "starting"
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/startingpage.jpg'
    FloatLayout:
        Label:
            text: "N"
            font_size: 130
            bold: True
            pos_hint: {"x":0.32, "top":0.8}
            size_hint: 0.35, 0.15
        Label:
            text: "Welcome to Nutricio"
            pos_hint: {"x": 0.29 , "y":0.5}
            size_hint: 0.4, 0.15
        Label:
            text: "Better Health For Better Future"
            pos_hint: {"x":0.32, "y":0.42}
            size_hint: 0.35, 0.24
        Button:
            pos_hint:{"x":0.34,"y":0.4}
            size_hint: 0.33, 0.05
            text: "GET STARTED"
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            on_release:
                root.manager.transition.direction = "right"
                root.start()

<LoginPage>:
    name: "login"
    username: username
    password: password
    canvas:
        Rectangle:
            pos: 0,210
            size: 382,320
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Login.png'
    FloatLayout:
        Label:
            text: "N"
            font_size: 130
            bold: True
            pos_hint: {"x":0.65, "top":0.96}
            size_hint: 0.35, 0.15
        Label:
            text: "Welcome to Nutricio"
            font_size: 20
            color: 0,0,0,1
            pos_hint: {"x": 0.29 , "y":0.6}
            size_hint: 0.4, 0.15
        TextInput:
            id:username
            multiline: False
            hint_text: "Email or Username"
            pos_hint: {"x":0.1, "top":0.63}
            size_hint: 0.8, 0.05
        TextInput:
            id:password
            multiline: False
            hint_text: "Password"
            pos_hint: {"x":0.1, "top":0.55}
            size_hint: 0.8, 0.05
        Button:
            pos_hint:{"x":0.1,"y":0.4}
            size_hint: 0.8, 0.05
            text: "Sign in"
            color: 1,1,1,1
            background_normal:''
            background_color: 251/255,178/255,67/255,1
            on_release:
                root.manager.transition.direction = "right"
                root.loginBtn()
        Button:
            pos_hint:{"x":0.1,"y":0.33}
            size_hint: 0.8, 0.05
            text: "Don\'t have an account? Register Now!"
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            on_release:
                root.manager.transition.direction = "right"
                root.createBtn()
        Label:
            text: "Login with"
            bold: True
            pos_hint: {"x": 0.29 , "y":0.1}
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Facebook_Icon.png'
            background_down: 'Background/Facebook_Icon.png'
            size_hint: 0.135, 0.073
            pos_hint: {"x":0.3, "y":0.06}
            on_press:
                root.facebook()
        Button:
            background_normal: 'Background/Google_Icon.png'
            background_down: 'Background/Google_Icon.png'
            size_hint: 0.135, 0.073
            pos_hint: {"x":0.54, "y":0.06}
            on_press:
                root.google()

<SignUpPage>:
    name: "signup"
    firstname: firstname
    lastname: lastname
    dateofbirth: dateofbirth
    weight: weight
    tall: tall
    email: email
    password: password

    canvas:
        Rectangle:
            pos: 0,0
            size: 382,570
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'

    FloatLayout:
        Label:
            text: "Sign Up"
            font_size: 25
            bold: True
            pos_hint: {"x":0.35, "top":1}
            size_hint: 0.35, 0.15
        Button:
            background_normal: 'Background/Profile_Icon.png'
            background_down: 'Background/Profile_Icon.png'
            size_hint: 0.2, 0.11
            pos_hint: {"x":0.42, "top":0.82}
            on_press:
                root.profile()
        TextInput:
            size_hint: 0.8, 0.05
            pos_hint: {"x":0.1, "top":0.68}
            hint_text: "First Name"
            id: firstname
            multiline: False
        TextInput:
            size_hint: 0.8, 0.05
            pos_hint: {"x":0.1, "top":0.61}
            hint_text: "Last Name"
            id: lastname
            multiline: False
        TextInput:
            pos_hint: {"x":0.1, "top":0.54}
            size_hint: 0.8, 0.05
            hint_text: "Date of Birth"
            id: dateofbirth
            multiline: False
        TextInput:
            size_hint: 0.38, 0.05
            pos_hint: {"x":0.1, "top":0.73-0.13*2}
            hint_text: "Weight"
            id: weight
            multiline: False
        TextInput:
            pos_hint: {"x":0.52, "top":0.73-0.13*2}
            size_hint: 0.38, 0.05
            hint_text: "Height"
            id: tall
            multiline: False
        TextInput:
            size_hint: 0.8, 0.05
            pos_hint: {"x":0.1, "top":0.4}
            hint_text: "Email"
            id: email
            multiline: False
        TextInput:
            pos_hint: {"x":0.1, "top":0.33}
            size_hint: 0.8, 0.05
            hint_text: "Password"
            id: password
            multiline: False
        Button:
            pos_hint:{"x":0.1,"y":0.18}
            size_hint: 0.8, 0.05
            text: "Already have an account? Log in now!"
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            on_release:
                root.manager.transition.direction = "left"
                root.login()
        Button:
            pos_hint:{"x":0.1,"y":0.12}
            size_hint: 0.8, 0.05
            text: "Sign Up"
            background_normal:''
            background_color: 251/255,178/255,67/255,1
            on_release:
                root.manager.transition.direction = "right"
                root.submit()
        Label:
            text: "By Proceeding you also agree to the Terms"
            font_size: 12
            color: 0,0,0,1
            pos_hint: {"x": 0.28 , "y":0.02}
            size_hint: 0.4, 0.15
        Label:
            text: "and Privacy Policy"
            font_size: 12
            color: 0,0,0,1
            pos_hint: {"x": 0.32 , "y":0.00}
            size_hint: 0.4, 0.15

<HomePage>:
    name: "home"
    canvas:
        Rectangle:
            pos: 0,500
            size: 382,320
        Rectangle:
            pos: 0,0
            size: 382,78
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Login.png'
    FloatLayout:
        cols: 1
        Button:
            text: "Log Out"
            size_hint: 0.2, 0.04
            color: 123/255, 177/255, 57/255, 1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0.8, "top":1}
            on_press:
                root.logOut()
        Label:
            text: "N"
            font_size: 130
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.32, "top":0.94}
            size_hint: 0.35, 0.15
        Label:
            text: "Nutricio"
            color: 123/255, 177/255, 57/255,1
            pos_hint: {"x": 0.29 , "y":0.7}
            size_hint: 0.4, 0.15
        Label:
            text: "Better Health For Better Future"
            color: 123/255, 177/255, 57/255,1
            pos_hint: {"x":0.32, "y":0.62}
            size_hint: 0.35, 0.24
        FloatLayout:
            Button:
                background_normal: 'Background/Scan_Icon.png'
                background_down: 'Background/Scan2_Icon.png'
                size_hint: 0.4, 0.2
                pos_hint: {"x":0.06, "y":0.46}
                on_press:
                    root.scan()
            Label:
                text: "Scan"
                pos_hint: {"x": 0.06, "y":0.37}
                size_hint: 0.4, 0.15
            Button:
                background_normal: 'Background/Report_Icon.png'
                background_down: 'Background/Report2_Icon.png'
                size_hint: 0.4, 0.2
                pos_hint: {"x":0.54, "y":0.46}
                on_press:
                    root.report()
            Label:
                text: "Report"
                pos_hint: {"x":0.54, "y":0.37}
                size_hint: 0.4, 0.15
            Button:
                background_normal: 'Background/Calculator_Icon.png'
                background_down: 'Background/Calculator2_Icon.png'
                size_hint: 0.4, 0.2
                pos_hint: {"x":0.06, "y":0.19}
                on_press:
                    root.calculator()
            Label:
                text: "Calculator"
                pos_hint: {"x":0.06, "y":0.1}
                size_hint: 0.4, 0.15
            Button:
                background_normal: 'Background/Setting_Icon.png'
                background_down: 'Background/Setting_Icon2.png'
                size_hint: 0.4, 0.2
                pos_hint: {"x":0.54, "y":0.19}
                on_press:
                    root.setting()
            Label:
                text: "Setting"
                pos_hint: {"x":0.54, "y":0.1}
                size_hint: 0.4, 0.15

        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<SettingPage>:
    name: "setting"
    canvas:
        Rectangle:
            pos: 0,0
            size: 382,78
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Label:
            text: "Setting"
            font_size: 25
            bold: True
            pos_hint: {"x":0.35, "top":1}
            size_hint: 0.35, 0.15
        Button:
            text: "Back"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<ScanPage>:
    name: "scan"
    canvas:
        Rectangle:
            pos: 0,0
            size: 382,78
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Label:
            text: "Scan"
            font_size: 25
            bold: True
            pos_hint: {"x":0.35, "top":1}
            size_hint: 0.35, 0.15
        Button:
            text: "Back"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Button:
            background_normal: 'Background/Scan_Icon3.png'
            background_down: 'Background/Scan_Icon3.png'
            size_hint: 0.79, 0.45
            pos_hint: {"x":0.12, "y":0.35}
            on_press:
                root.manager.transition.direction = "left"
                root.scan()
        Label:
            text: "Tap or click to scan"
            pos_hint: {"x":0.32, "top":0.65}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        MDRaisedButton:
            size_hint: 0.8, 0.05
            size: 3 * dp(48), dp(48)
            text: 'Calculate Now!'
            md_bg_color: 251/255,178/255,67/255,1
            pos_hint:{"x":0.1,"y":0.2}
            on_release: 
                root.manager.transition.direction = "right"
                root.calculate()
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<FinalResultPage>:
    name: "final"
    food: food
    image: image
    info: info
    calories: calories
    protein: protein
    carbohydrate: carbohydrate
    totalfat: totalfat
    vitaminc: vitaminc
    
    canvas:
        Rectangle:
            pos: 0,360
            size: 382,450
        Rectangle:
            pos: 0,0
            size: 382,78
        Ellipse:
            pos: 140,320
            size: 100,100
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "N"
            font_size: 100
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.32, "top":0.6}
            size_hint: 0.35, 0.15
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            text: "Tap"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.calculate()
        Label:
            id: food
            text: ""
            font_size: 26
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.3, "top":1}
            size_hint: 0.35, 0.15
        Label:
            id: info
            text: ""
            font_size: 16
            text_size: self.width, None
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0, "top":0.69}
            size_hint: 1, None
            height: self.texture_size[1]
        Image:
            id: image
            source: ""
            size_hint: 0.4,0.4
            pos_hint: {"x":0.3, "top":0.99}
        Label:
            text: "Calories"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.48}
            size_hint: 0.35, 0.15
        Label:
            id: calories
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.48}
            size_hint: 0.35, 0.15
        Label:
            text: "Protein"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.42}
            size_hint: 0.35, 0.15
        Label:
            id: protein
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.42}
            size_hint: 0.35, 0.15
        Label:
            text: "Carbohydrate"
            font_size: 20
            bold: True
            pos_hint: {"x":0.05, "top":0.36}
            size_hint: 0.35, 0.15
        Label:
            id: carbohydrate
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.65, "top":0.36}
            size_hint: 0.35, 0.15
        Label:
            text: "Total Fat"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.3}
            size_hint: 0.35, 0.15
        Label:
            id: totalfat
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.3}
            size_hint: 0.35, 0.15
        Label:
            text: "Vitamin C"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.24}
            size_hint: 0.35, 0.15
        Label:
            id: vitaminc
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.24}
            size_hint: 0.35, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<ReportPage>:
    name: "report"
    calories: calories
    protein: protein
    carbohydrate: carbohydrate
    totalfat: totalfat
    vitaminc: vitaminc
    canvas:
        Rectangle:
            pos: 0,620
            size: 382,220
        Rectangle:
            pos: 0,0
            size: 382,78
        Ellipse:
            pos: 140,570
            size: 100,100
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Label:
            text: "Report"
            font_size: 25
            bold: True
            pos_hint: {"x":0.35, "top":1}
            size_hint: 0.35, 0.15
        Button:
            text: "Back"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Button:
            text: "Tap"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0.8, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.calculate()
        Label:
            text: "N"
            font_size: 100
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.32, "top":0.93}
            size_hint: 0.35, 0.15
        Label:
            text: "Weekly Report"
            font_size: 25
            bold: True
            pos_hint: {"x":0.33, "top":0.8}
            size_hint: 0.35, 0.15
        Label:
            text: "Calories"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.74}
            size_hint: 0.35, 0.15
        Label:
            id: calories
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.74}
            size_hint: 0.35, 0.15
        Label:
            text: "Protein"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.68}
            size_hint: 0.35, 0.15
        Label:
            id: protein
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.68}
            size_hint: 0.35, 0.15
        Label:
            text: "Carbohydrate"
            font_size: 20
            bold: True
            pos_hint: {"x":0.05, "top":0.62}
            size_hint: 0.35, 0.15
        Label:
            id: carbohydrate
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.65, "top":0.62}
            size_hint: 0.35, 0.15
        Label:
            text: "Total Fat"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.56}
            size_hint: 0.35, 0.15
        Label:
            id: totalfat
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.56}
            size_hint: 0.35, 0.15
        Label:
            text: "Vitamin C"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.5}
            size_hint: 0.35, 0.15
        Label:
            id: vitaminc
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.5}
            size_hint: 0.35, 0.15
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<CalculatorPage>:
    name: "calculator"
    canvas:
        Rectangle:
            pos: 0,500
            size: 382,250
        Rectangle:
            pos: 0,0
            size: 382,78
        Rectangle:
            pos: 100,500
            size: 190,88
            source: 'Background/Food_Image.png'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Label:
            text: "Nutricio Calculator"
            font_size: 25
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.35, "top":1}
            size_hint: 0.35, 0.15
        Label:
            text: "What did you eat today?"
            font_size: 16
            color: 0,0,0,1
            pos_hint: {"x":0.35, "top":0.93}
            size_hint: 0.35, 0.15
        Button:
            text: "Back"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        MDRoundFlatIconButton:
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .6}
            on_release: 
                app.file_manager_open()
        MDRoundFlatIconButton:
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: 
                app.file_manager_open()
        MDRaisedButton:
            size_hint: None, None
            size: 3 * dp(48), dp(40)
            text: 'Calculate Now'
            md_bg_color:251/255,178/255,67/255,1
            pos_hint: {'center_x': .5, 'center_y': .2}
            on_release: root.process_button_click()
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<CalculatorResultPage>:
    name: "dailyReport"
    calories: calories
    protein: protein
    carbohydrate: carbohydrate
    totalfat: totalfat
    vitaminc: vitaminc
    dates:dates
    canvas:
        Rectangle:
            pos: 0,620
            size: 382,220
        Rectangle:
            pos: 0,0
            size: 382,78
        Ellipse:
            pos: 140,570
            size: 100,100
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Label:
            text: "Result"
            font_size: 20
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.33, "top":1}
            size_hint: 0.35, 0.15
        Button:
            text: "Tap"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.calculate()
        Label:
            text: "N"
            font_size: 100
            color: 123/255, 177/255, 57/255,1
            bold: True
            pos_hint: {"x":0.32, "top":0.93}
            size_hint: 0.35, 0.15
        Label:
            text: "Today History"
            font_size: 25
            bold: True
            pos_hint: {"x":0.33, "top":0.8}
            size_hint: 0.35, 0.15
        Label:
            text: "Calories"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.74}
            size_hint: 0.35, 0.15
        Label:
            id: calories
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.74}
            size_hint: 0.35, 0.15
        Label:
            text: "Protein"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.68}
            size_hint: 0.35, 0.15
        Label:
            id: protein
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.68}
            size_hint: 0.35, 0.15
        Label:
            text: "Carbohydrate"
            font_size: 20
            bold: True
            pos_hint: {"x":0.05, "top":0.62}
            size_hint: 0.35, 0.15
        Label:
            id: carbohydrate
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.65, "top":0.62}
            size_hint: 0.35, 0.15
        Label:
            text: "Total Fat"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.56}
            size_hint: 0.35, 0.15
        Label:
            id: totalfat
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.56}
            size_hint: 0.35, 0.15
        Label:
            text: "Vitamin C"
            font_size: 20
            bold: True
            pos_hint: {"x":0, "top":0.5}
            size_hint: 0.35, 0.15
        Label:
            id: vitaminc
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.6, "top":0.5}
            size_hint: 0.35, 0.15
        Label:
            id: dates
            text: ""
            font_size: 20
            bold: True
            pos_hint: {"x":0.31, "top":0.3}
            size_hint: 0.35, 0.15
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15

<SettingPage>:
    name: "setting"
    canvas:
        Rectangle:
            pos: 0,0
            size: 382,78
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Background/Sign Up.png'
    FloatLayout:
        Label:
            text: "Setting"
            font_size: 25
            bold: True
            pos_hint: {"x":0.35, "top":1}
            size_hint: 0.35, 0.15
        Button:
            text: "Back"
            size_hint: 0.2, 0.04
            color: 0,0,0,1
            background_color: 255,255,255,0.9
            pos_hint: {"x":0, "top":1}
            on_press:
                root.manager.transition.direction = "left"
                root.home()

        MDList:
            pos_hint: {"x":0, "top":0.86}
            OneLineListItem:
                Button:
                    text: "Edit Profile"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "Log Out"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
                    on_press:
                        root.logout()
            OneLineListItem:
                Button:
                    text: "Delete Account"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "Switch Account"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "Change Password"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "Reminders"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "Push Notifications"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "Privacy Settings"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "About Us"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
            OneLineListItem:
                Button:
                    text: "FAQs/Feedback"
                    pos_hint: {"x":0, "top":0.8}
                    color: 0,0,0,1
                    background_color: 255,255,255,0.9
        Button:
            background_normal: 'Background/Home_Icon.png'
            background_down: 'Background/Home2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.14, "y":0.04}
            on_press:
                root.manager.transition.direction = "left"
                root.home()
        Label:
            text: "Home"
            pos_hint: {"x":0, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Analytics_Icon.png'
            background_down: 'Background/Analytics2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.44, "y":0.04}
            on_press:
                root.report()
        Label:
            text: "Report"
            pos_hint: {"x":0.3, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
        Button:
            background_normal: 'Background/Editprofile_Icon.png'
            background_down: 'Background/Editprofile2_Icon.png'
            size_hint: 0.1, 0.05
            pos_hint: {"x":0.74, "y":0.04}
            on_press:
                root.setting()
        Label:
            text: "Profile"
            pos_hint: {"x":0.59, "top":0.1}
            color: 123/255, 177/255, 57/255, 1
            size_hint: 0.4, 0.15
"""

def toast(text):
    from kivymd.toast.kivytoast import toast
    toast(text)

class StartingPage(Screen):
    def start(self):
        self.manager.current = 'login'

class LoginPage(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.username.text, self.password.text):
            HomePage.current = self.username.text
            self.reset()
            self.manager.current = 'home'
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        self.manager.current = 'signup'

    def reset(self):
        self.username.text = ""
        self.password.text = ""

    def facebook(self):
        webbrowser.open("https://www.facebook.com/")

    def google(self):
        webbrowser.open("https://www.google.com/")

class SignUpPage(Screen):
    firstname = ObjectProperty(None)
    lastname = ObjectProperty(None)
    dateofbirth = ObjectProperty(None)
    weight = ObjectProperty(None)
    tall = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.firstname.text != "" and self.lastname.text != "" and self.dateofbirth.text != "" and self.weight.text != "" and self.tall.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.firstname.text, self.lastname.text)
                self.reset()
                self.manager.current = 'login'
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        self.manager.current = 'login'

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.firstname.text = ""
        self.lastname.text = ""
        self.dateofbirth.text = ""
        self.weight.text = ""
        self.tall.text = ""

    def profile(self):
        pass

class HomePage(Screen):
    def scan(self):
        self.manager.current = 'scan'

    def calculator(self):
        self.manager.current = 'calculator'

    def report(self):
        self.manager.current = 'report'

    def setting(self):
        self.manager.current = 'setting'

    def home(self):
        self.manager.current = 'home'

    def logOut(self):
        self.manager.current = 'login'

class ScanPage(Screen):
    def scan(self):
        video_capture = cv2.VideoCapture(0)
        cv2.namedWindow("test")
        img_counter = 0

        while(video_capture.isOpened()):
            ret, frame = video_capture.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)
            k = cv2.waitKey(1)
            if k % 256 == 27:
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                global img_name
                img_name = "Scanned Image/image{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
                self.calculate()
        video_capture.release()
        cv2.destroyAllWindows()

    def calculate(self):
        K.clear_session()
        model = keras.models.load_model('Model/model_trained_5class.hdf5',compile=False)
        food_list = ['beef_rendang', 'chicken_satay', 'fried_rice', 'gado_gado', 'omelette']
        images = []
        images.append(img_name)
        for img in images:
            img = image.load_img(img, target_size=(299, 299))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.

            pred = model.predict(img)
            index = np.argmax(pred)
            food_list.sort()
            global pred_value
            pred_value = food_list[index]
            self.manager.current = 'final'
            print(pred_value)

    def report(self):
        self.manager.current = 'final'

    def setting(self):
        self.manager.current = 'setting'

    def home(self):
        self.manager.current = 'home'

class FinalResultPage(Screen):
    def calculate(self):
        food_info = [["Rendang", img_name, "Rendang adalah masakan daging yang berasal dari Minangkabau. Masakan ini dihasilkan dari proses memasak suhu rendah dalam waktu lama menggunakan aneka rempah-rempah dan santan.", "545 kkal", "48 gr", "13 gr", "36 gr", "0 mg"],
                    ["Sate", img_name, "Sate adalah makanan yang terbuat dari daging yang dipotong kecil-kecil dan ditusuk sedemikian rupa dengan tusukan lidi tulang daun kelapa atau bambu kemudian dipanggang menggunakan bara arang kayu. ", "272 kkal", "23.73 gr", "5.84 gr", "17.76 gr", "0 mg"],
                    ["Nasi Goreng", img_name, "Nasi goreng adalah sajian nasi yang digoreng dalam sebuah wajan atau penggorengan menghasilkan cita rasa berbeda karena dicampur dengan bumbu-bumbu.", "238 kkal", "5.5 gr", "45 gr", "4.1 gr", "0 mg"],
                    ["Gado Gado", img_name, "Gado gado adalah salah satu makanan khas yang berasal dari Indonesia yang berupa sayur-sayuran yang direbus dan dicampur jadi satu, dengan bumbu kacang.", "132 kkal", "6,10 gr", "21 gr", "3,20 gr", "19.7 mg"],
                    ["Telur Dadar", img_name, "Telur dadar adalah variasi hidangan telur goreng yang disiapkan dengan cara mengocok telur dan menggorengnya dengan minyak goreng atau mentega panas di sebuah wajan.", "93 kkal", "6,48 gr", "0,42 gr", "7,33 gr", "0 mg"]
                    ]

        if pred_value == "beef_rendang":
            i = 0
        elif pred_value == "chicken_satay":
            i = 1
        elif pred_value == "fried_rice":
            i = 2
        elif pred_value == "gado_gado":
            i = 3
        elif pred_value == "omelette":
            i = 4

        self.food.text = food_info[i][0]
        self.image.source = food_info[i][1]
        self.info.text = food_info[i][2]
        self.calories.text = food_info[i][3]
        self.protein.text = food_info[i][4]
        self.carbohydrate.text = food_info[i][5]
        self.totalfat.text = food_info[i][6]
        self.vitaminc.text = food_info[i][7]

    def report(self):
        self.manager.current = 'report'
    def setting(self):
        self.manager.current = 'setting'
    def home(self):
        self.manager.current = 'home'

class CalculatorPage(Screen):
    img_path = ObjectProperty(None)
    msg = ObjectProperty(None)

    def process_button_click(self):
        mythread = threading.Thread(target=self.food_detection())
        mythread.start()

    def food_detection(self):

        K.clear_session()
        model = keras.models.load_model('Model/model_trained_5class.hdf5', compile=False)
        food_list = ['beef_rendang', 'chicken_satay', 'fried_rice', 'gado_gado', 'omelette']

        images = []

        with open('path.txt') as f:
            for line in f:
                # For Python3, use print(line)
                txt = line.split()
                images.append(txt[0])
                if 'str' in line:
                    break
        os.remove("path.txt")

        global pred_values
        pred_values = []

        for img in images:
            img = image.load_img(img, target_size=(299, 299))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.

            pred = model.predict(img)
            index = np.argmax(pred)
            food_list.sort()
            global pred_value
            pred_value = food_list[index]
            pred_values.append(pred_value)

        self.manager.current = 'dailyReport'

    def report(self):
        self.manager.current = 'report'

    def setting(self):
        self.manager.current = 'setting'

    def home(self):
        self.manager.current = 'home'

class CalculatorResultPage(Screen):
    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    def calculate(self):
        food_info = [["Rendang","545", "48", "13", "36", "0"],
                     ["Sate", "272", "23.73", "5.84", "17.76", "0"],
                     ["Nasi Goreng","238", "5.5", "45", "4.1", "19.7"],
                     ["Gado Gado", "132", "6.10", "21", "3.20", "1"],
                     ["Telur Dadar","93", "6.48", "0.42", "7.33", "0"]
                     ]
        sum = [0,0,0,0,0]
        for i in pred_values:
            if i == "beef_rendang":
                sum[0] += float(food_info[0][1])
                sum[1] += float(food_info[0][2])
                sum[2] += float(food_info[0][3])
                sum[3] += float(food_info[0][4])
                sum[4] += float(food_info[0][5])
            elif i == "chicken_satay":
                sum[0] += float(food_info[1][1])
                sum[1] += float(food_info[1][2])
                sum[2] += float(food_info[1][3])
                sum[3] += float(food_info[1][4])
                sum[4] += float(food_info[1][5])
            elif i == "fried_rice":
                sum[0] += float(food_info[2][1])
                sum[1] += float(food_info[2][2])
                sum[2] += float(food_info[2][3])
                sum[3] += float(food_info[2][4])
                sum[4] += float(food_info[2][5])
            elif i == "gado_gado":
                sum[0] += float(food_info[3][1])
                sum[1] += float(food_info[3][2])
                sum[2] += float(food_info[3][3])
                sum[3] += float(food_info[3][4])
                sum[4] += float(food_info[3][5])
            elif i == "omelette":
                sum[0] += float(food_info[4][1])
                sum[1] += float(food_info[4][2])
                sum[2] += float(food_info[4][3])
                sum[3] += float(food_info[4][4])
                sum[4] += float(food_info[4][5])

        self.calories.text = str(sum[0]) + " kkal"
        self.protein.text = str(sum[1]) + " gr"
        self.carbohydrate.text = str(sum[2]) + " gr"
        self.totalfat.text = str(sum[3]) + " gr"
        self.vitaminc.text = str(sum[4]) + " mg"

        self.dates.text = self.get_date()

        f = open("Weekly Report.txt", "a")
        f.write("{} {} {} {} {} {}\n".format(self.dates.text,sum[0],sum[1],sum[2],sum[3],sum[4]))
        f.close()

    def report(self):
        self.manager.current = 'report'

    def setting(self):
        self.manager.current = 'setting'

    def home(self):
        self.manager.current = 'home'

class ReportPage(Screen):

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    def calculate(self):
        from datetime import datetime
        with open('Weekly Report.txt') as f:
            sums = [0, 0, 0, 0, 0]
            for line in f:
                txt = line.split()
                dx = self.get_date()
                dy = txt[0]
                d1 = datetime.strptime(dy, "%Y-%m-%d")
                d2 = datetime.strptime(dx, "%Y-%m-%d")
                diff = abs((d2 - d1).days)
                if diff > 7:
                    continue
                print(diff)

                sums[0] += float(txt[1])
                sums[1] += float(txt[2])
                sums[2] += float(txt[3])
                sums[3] += float(txt[4])
                sums[4] += float(txt[5])
                print(sums[0])

                self.calories.text = str(format(sums[0], '.2f')) + " kkal"
                self.protein.text = str(format(sums[1], '.2f')) + " gr"
                self.carbohydrate.text = str(format(sums[2], '.2f')) + " gr"
                self.totalfat.text = str(format(sums[3], '.2f')) + " gr"
                self.vitaminc.text = str(format(sums[4], '.2f')) + " mg"

                if 'str' in line:
                    break

    #             self.parameter.source = self.show_param()
    #
    # def show_param(self):
    #     data = [("Mr T", 45, 105)]
    #     limits = [20, 60, 100, 160]
    #     labels = ["Poor", "OK", "Good", "Excellent"]
    #     size = (8, 5)
    #     axis_label = "Performance Measure"
    #     label_color = "black"
    #     bar_color = "#252525"
    #     target_color = '#f7f7f7'
    #     title = "Sales Rep Performance"
    #     palette = None
    #     formatter = None
    #
    #     h = limits[-1] / 10
    #
    #     # Use the green palette as a sensible default
    #     if palette is None:
    #         palette = sns.light_palette("green", len(limits), reverse=False)
    #
    #     # Must be able to handle one or many data sets via multiple subplots
    #     if len(data) == 1:
    #         fig, ax = plt.subplots(figsize=size, sharex=True)
    #     else:
    #         fig, axarr = plt.subplots(len(data), figsize=size, sharex=True)
    #
    #     # Add each bullet graph bar to a subplot
    #     for idx, item in enumerate(data):
    #
    #         # Get the axis from the array of axes returned when the plot is created
    #         if len(data) > 1:
    #             ax = axarr[idx]
    #
    #         # Formatting to get rid of extra marking clutter
    #         ax.set_aspect('equal')
    #         ax.set_yticklabels([item[0]])
    #         ax.set_yticks([1])
    #         ax.spines['bottom'].set_visible(False)
    #         ax.spines['top'].set_visible(False)
    #         ax.spines['right'].set_visible(False)
    #         ax.spines['left'].set_visible(False)
    #
    #         prev_limit = 0
    #         for idx2, lim in enumerate(limits):
    #             # Draw the bar
    #             ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
    #                     color=palette[idx2])
    #             prev_limit = lim
    #         rects = ax.patches
    #         # The last item in the list is the value we're measuring
    #         # Draw the value we're measuring
    #         ax.barh([1], item[1], height=(h / 3), color=bar_color)
    #
    #         # Need the ymin and max in order to make sure the target marker
    #         # fits
    #         ymin, ymax = ax.get_ylim()
    #         ax.vlines(
    #             item[2], ymin * .9, ymax * .9, linewidth=1.5, color=target_color)
    #
    #     # Now make some labels
    #     if labels is not None:
    #         for rect, label in zip(rects, labels):
    #             height = rect.get_height()
    #             ax.text(
    #                 rect.get_x() + rect.get_width() / 2,
    #                 -height * .4,
    #                 label,
    #                 ha='center',
    #                 va='bottom',
    #                 color=label_color)
    #     if formatter:
    #         ax.xaxis.set_major_formatter(formatter)
    #     if axis_label:
    #         ax.set_xlabel(axis_label)
    #     if title:
    #         fig.suptitle(title, fontsize=14)
    #     fig.subplots_adjust(hspace=0)


    def report(self):
        self.manager.current = 'report'

    def setting(self):
        self.manager.current = 'setting'

    def home(self):
        self.manager.current = 'home'

class SettingPage(Screen):
    def report(self):
        self.manager.current = 'report'

    def setting(self):
        self.manager.current = 'setting'

    def home(self):
        self.manager.current = 'home'

    def logout(self):
        self.manager.current = 'login'

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login', content=Label(text='Invalid username or password.'), size_hint=(None, None),
                size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form', content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


db = DataBase("users.txt")
sm = WindowManager()

screens = [StartingPage(name="starting"), LoginPage(name="login"), SignUpPage(name="signup"), HomePage(name="home"),
           ScanPage(name="scan"), FinalResultPage(name="final"), ReportPage(name="report"), CalculatorPage(name="calculator"),
           SettingPage(name="setting"), CalculatorResultPage(name="dailyReport")]
for x in screens:
    sm.add_widget(x)


class MainApp(MDApp):
    title = "Nutricio"
    Window.size = (382, 729)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivymd.uix.filemanager import MDFileManager
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
        )

    def file_manager_open(self):
        self.file_manager.show('C:/Users/Firmaulana/Desktop/Nutricio/CaptureImage')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        f = open("path.txt", "a")
        f.write("{} \n".format(path))
        f.close()
        toast(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

if __name__ == "__main__":
    MainApp().run()