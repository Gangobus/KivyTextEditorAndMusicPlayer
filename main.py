#main.py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Window import WindowInterface
import multiprocessing
from VoiceRecognition import VoiceToText
from kivy.clock import Clock
class MainApp(MDApp):
    def build(self):
        print('mainprocess1')
        Window.size = [1600, 800]
        self.compare_mode = False
        self.highlight_color = (255, 0, 0, 1)  # set highlight color
        Builder.load_file("w1txt.kv")

        sm = ScreenManager()
        sm.add_widget(WindowInterface(name="S1T"))

        # if multiprocessing.current_process().name == 'build':
        #     process = multiprocessing.Process(target=VoiceToText.run_spech_recogn)
        #     process.start()

        return sm

def run_app():
    MainApp().run()

if __name__ == '__main__':
    run_app()
