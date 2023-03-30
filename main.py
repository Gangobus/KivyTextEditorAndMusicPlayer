import os
from kivy.clock import Clock
from tkinter import Tk, filedialog
from docx import Document
from kivymd.uix.button import MDIconButton
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen, ScreenManager
from Window1txt import Window1txt
from Window2txt import Window2txt
class MainApp(MDApp):
    def build(self):
        Window.size = [1600, 800]
        LabelBase.register(name='TimesNewRoman',
                           fn_regular='times-new-roman.ttf')
        self.compare_mode = False
        self.highlight_color = (255, 0, 0, 1)  # set highlight color

        Builder.load_file("w2txt.kv")
        Builder.load_file("w1txt.kv")

        sm=ScreenManager()
        sm.add_widget(Window1txt(name="S1T"))
        sm.add_widget(Window2txt(name="S2T"))
        return sm
    def fps_check(self):
        self.fps_monitor_start()

MainApp().run()