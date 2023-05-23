from tkinter import Tk, filedialog
from docx import Document
from kivy.uix.boxlayout import BoxLayout
from VoiceRecognition import VoiceToText
import keyboard
from kivy.clock import Clock

class SecondText(BoxLayout):
    def open_22_file_dialog(self, *args):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            if file_path.endswith(".docx"):
                document = Document(file_path)
                self.ids.txt22.text = "\n".join([para.text for para in document.paragraphs])
            else:
                with open(file_path, 'r+', encoding='utf-8') as file:
                    self.ids.txt22.text = file.read()

    def save_22_text_to_file(self, *args):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.ids.txt22.text)
                # Если файл имеет расширение .docx, то сохраняем его в формате docx
                if file_path.endswith(".docx"):
                    document = Document()
                    document.add_paragraph(self.ids.txt22.text)
                    document.save(file_path)

    def increase_font_size2(self):
        self.ids.txt22.font_size += 2

    # метод для уменьшения размера шрифта
    def decrease_font_size2(self):
        self.ids.txt22.font_size -= 2

class TxtFunctions():
    def spech_to_text(self):
        if self.voicetext in self.ids.bta.children:
            self.ids.bta.remove_widget(self.voicetext)
            # self.ids.textbuttonsarea.remove_widget(self.widgfinddiff)
            # self.ids.textbuttonsarea.remove_widget(self.widgremdeif)
        else:
            self.ids.bta.add_widget(self.voicetext)

    def txt2(self):
        secondtext = SecondText()
        if self.secondtext in self.ids.bta.children:
            self.ids.bta.remove_widget(self.secondtext)
            # self.ids.textbuttonsarea.remove_widget(self.widgfinddiff)
            # self.ids.textbuttonsarea.remove_widget(self.widgremdeif)
        else:
            self.ids.bta.add_widget(self.secondtext)
            # self.ids.textbuttonsarea.add_widget(self.widgfinddiff)
            # self.ids.textbuttonsarea.add_widget(self.widgremdeif)

    def open_txt_file_dialog(self, *args):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            if file_path.endswith(".docx"):
                document = Document(file_path)
                self.ids.txt1.text = "\n".join([para.text for para in document.paragraphs])
            else:
                with open(file_path, 'r+', encoding='cp1251') as file:
                    self.ids.txt1.text = file.read()

    def save_text_to_file(self, *args):
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

    def add_text_to_input(self):
        print(self.ids.txt1.text)

        a1 = self.ids.txt1.text
        print(a1)
        a1 += "<M1>"
        print(a1)
        self.ids.txt1.text = a1
        print(self.ids.txt1.text)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secondtext = SecondText()
        self.voicetext = VoiceToText()
        keyboard.add_hotkey("Ctrl + 1", self.add_text_to_input)




