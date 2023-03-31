
from kivy.uix.screenmanager import Screen
from musicplayer import TopMusicBar
from TxtFunc import TxtFunctions

class Window2txt(TxtFunctions, Screen, TopMusicBar):
    def on_start(self):
        self.paused = True
        self.current_pos = 0
        self.song_time = 0
        self.update_time = None
        self.sound = None

