from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Window1txt import Window1txt

class MainApp(MDApp):
    def build(self):
        Window.size = [1600, 800]
        self.compare_mode = False
        self.highlight_color = (255, 0, 0, 1)  # set highlight color
        Builder.load_file("musicplayer.kv")
        Builder.load_file("w1txt.kv")

        sm=ScreenManager()
        sm.add_widget(Window1txt(name="S1T"))
        return sm

MainApp().run()