# main.py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Window import WindowInterface

class MainApp(MDApp):
    def build(self):
        print('mainprocess1')
        Window.size = [1600, 800]
        self.compare_mode = False
        self.highlight_color = (255, 0, 0, 1)
        Builder.load_file("w1txt.kv")

        sm = ScreenManager()
        sm.add_widget(WindowInterface(name="S1T"))

        return sm

def run_app():
    MainApp().run()

if __name__ == '__main__':
    run_app()