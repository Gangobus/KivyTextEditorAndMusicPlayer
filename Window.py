#Window.py
from kivy.uix.screenmanager import Screen
from MediaModule import Sound
from TextModule import Text1Func
from kivy.clock import Clock
import keyboard

#класс  для интерфейса(окна)
class WindowInterface(Text1Func, Screen, Sound):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sound = Sound()
        self.hotkeys_event = None
        self.hotkeys_event = Clock.schedule_once(self.text_keys)

    #привязка горячих клваиш
    def text_keys(self, *args):
        print("text_keys")
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey("Ctrl+`", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+`'],))
        keyboard.add_hotkey("Ctrl+1", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+1'],))
        keyboard.add_hotkey("Ctrl+2", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+2'],))
        keyboard.add_hotkey("Ctrl+3", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+3'],))
        keyboard.add_hotkey("Ctrl+4", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+4'],))
        keyboard.add_hotkey("Ctrl+5", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+5'],))
        keyboard.add_hotkey("Ctrl+6", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+6'],))
        keyboard.add_hotkey("Ctrl+7", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+7'],))
        keyboard.add_hotkey("Ctrl+8", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+8'],))
        keyboard.add_hotkey("Ctrl+9", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+9'],))
        keyboard.add_hotkey("Ctrl+0", self.insert_text_from_shortcut, args=(self.shortcut_labels['Ctrl+0'],))
        keyboard.add_hotkey("Alt+`", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+`'],))
        keyboard.add_hotkey("Alt+1", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+1'],))
        keyboard.add_hotkey("Alt+2", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+2'],))
        keyboard.add_hotkey("Alt+3", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+3'],))
        keyboard.add_hotkey("Alt+4", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+4'],))
        keyboard.add_hotkey("Alt+5", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+5'],))
        keyboard.add_hotkey("Alt+6", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+6'],))
        keyboard.add_hotkey("Alt+7", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+7'],))
        keyboard.add_hotkey("Alt+8", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+8'],))
        keyboard.add_hotkey("Alt+9", self.insert_text_from_shortcut, args=(self.shortcut_labels['Alt+9'],))
        keyboard.add_hotkey("Alt+0", self.print_formatted_time)
        keyboard.add_hotkey("F1", self.playandpause)
        keyboard.add_hotkey("F3", self.rewindplus)
        keyboard.add_hotkey("F2", self.rewindminus)
        keyboard.add_hotkey("F4", self.playandpause)