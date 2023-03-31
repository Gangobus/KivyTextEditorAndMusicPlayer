
from kivy.uix.screenmanager import Screen
from musicplayer import TopMusicBar
from TxtFunc import TxtFunctions

class Window1txt(TxtFunctions, Screen, TopMusicBar):
    def on_start(self):
        self.fps_monitor_start()

