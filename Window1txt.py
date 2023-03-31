import os
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
from docx import Document
from musicplayer import TopMusicBar
from TxtFunc import TxtFunctions

class Window1txt(TxtFunctions, Screen, TopMusicBar):
    def on_start(self):
        self.fps_monitor_start()

