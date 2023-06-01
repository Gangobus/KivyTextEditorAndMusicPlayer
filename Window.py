from kivy.uix.screenmanager import Screen
from musicplayer import TopMusicBar
from TxtFunc import TxtFunctions


class WindowInterface(TxtFunctions, Screen, TopMusicBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        top_music_bar = TopMusicBar()