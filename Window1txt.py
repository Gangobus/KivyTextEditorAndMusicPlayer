import os
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
from docx import Document
from kivy.clock import Clock


class Window1TxtFunctions():
    def open_txt_file_left_dialog(self, *args):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            if file_path.endswith(".docx"):
                document = Document(file_path)
                self.ids.txt1.text = "\n".join([para.text for para in document.paragraphs])
            else:
                with open(file_path, 'r+', encoding='utf-8') as file:
                    self.ids.txt1.text = file.read()

    def save_left_text_to_file(self, *args):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.ids.txt1.text)
                # Если файл имеет расширение .docx, то сохраняем его в формате docx
                if file_path.endswith(".docx"):
                    document = Document()
                    document.add_paragraph(self.ids.txt1.text)
                    document.save(file_path)

    # метод для увеличения размера шрифта
    def increase_font_size1(self):
        self.ids.txt1.font_size += 2

    # метод для уменьшения размера шрифта
    def decrease_font_size1(self):
        self.ids.txt1.font_size -= 2


class Window1txt(Window1TxtFunctions, Screen):
    def on_start(self):
        self.fps_monitor_start()
    def init(self, **kwargs):
        super().init(**kwargs)
        self.sound = None
        self.song_time = 0
        self.seek_slider = self.ids.seek_slider
        self.play_button = self.ids.play_pause_button
        self.timer_event = None
        self.init_player()



