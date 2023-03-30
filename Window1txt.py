import os
from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
from docx import Document
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class Window1TxtFunctions():
    def fps_check(self):
        self.fps_monitor_start()

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
        self.paused = True
        self.current_pos = 0
        self.song_time = 0
        self.update_time = None
        self.sound = None



    # def choose_file(self, instance):
    #     # открыть диалоговое окно выбора файла
    #     try:
    #         path = os.path.dirname(os.path.abspath(__file__))
    #     except NameError:
    #         path = os.getcwd()
    #     file_name = self.file_chooser_dialog(path)
    #     if file_name:
    #         # загрузить звуковой файл
    #         self.sound = SoundLoader.load(file_name)
    #         self.song_time = 0
    #
    # def file_chooser_dialog(self, path):
    #     # открыть диалоговое окно выбора файла
    #     try:
    #         from tkinter import Tk
    #         from tkinter.filedialog import askopenfilename
    #     except ImportError:
    #         return None
    #     Tk().withdraw()
    #     file_name = askopenfilename(initialdir=path,
    #                                 title="Выберите MP3 файл",
    #                                 filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
    #
    # def play_pause(self, instance):
    #     if self.sound:
    #         if self.paused:
    #             self.sound.play()
    #             self.paused = False
    #             self.update_time = Clock.schedule_interval(self.update_progress, 0.1)
    #             instance.icon = "pause"
    #         else:
    #             self.sound.stop()
    #             self.paused = True
    #             Clock.unschedule(self.update_time)
    #             instance.icon = "play"
    #
    # def rewind(self, instance):
    #     if self.sound:
    #         self.current_pos = max(self.current_pos - 5, 0)
    #         self.sound.seek(self.current_pos)
    #
    # def fast_forward(self, instance):
    #     if self.sound:
    #         self.current_pos = min(self.current_pos + 5, self.sound.length)
    #         self.sound.seek(self.current_pos)
    #
    # def mute(self, instance):
    #     if self.sound:
    #         self.sound.volume = 0 if self.sound.volume > 0 else 1
    #         instance.icon = "volume-off" if self.sound.volume == 0 else "volume-mute"
    #
    # def update_progress(self, dt):
    #     if self.sound:
    #         self.current_pos = self.sound.get_pos()
    #         self.ids.current_time.text = self.format_time(self.current_pos)
    #         self.ids.progress.value = self.current_pos / self.sound.length
    #
    # def format_time(self, seconds):
    #     # helper method to format time in seconds to hh:mm:ss
    #     return f"{int(seconds // 3600):02d}:{int((seconds // 60) % 60):02d}:{int(seconds % 60):02d}"


