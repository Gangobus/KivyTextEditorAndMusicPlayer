from kivy.uix.screenmanager import Screen
from VoiceRecognition import VoiceToText
from musicplayer import TopMusicBar
from TxtFunc import TxtFunctions
import keyboard


class WindowInterface(VoiceToText, TxtFunctions, Screen, TopMusicBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

