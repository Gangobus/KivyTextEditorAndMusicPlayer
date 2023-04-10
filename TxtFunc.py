from multiprocessing import Process
import threading
import os
from tkinter import Tk, filedialog
from docx import Document
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
import wave
import json
import vosk
from pydub import AudioSegment

class VoiceText(BoxLayout):
    def spech_recogn(self):
        # Open a file dialog box to select the input audio file
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[('Video Files', '*.mp4'), ('MP3 Files', '*.mp3'), ('OGG Files', '*.ogg'), ('WAV Files', '*.wav'),
                       ('All Files', '*.*')]
        )

        # Convert non-WAV files to WAV with a sample rate of 8000
        audio_format = os.path.splitext(file_path)[1]
        if audio_format != ".wav":
            sound = AudioSegment.from_file(file_path, format=audio_format[1:])
            sound = sound.set_frame_rate(8000).set_channels(1)
            file_path = os.path.splitext(file_path)[0] + ".wav"
            sound.export(file_path, format="wav")
        elif file_path.endswith(".mp4"):
            # Convert MP4 file to WAV with a sample rate of 8000
            sound = AudioSegment.from_file(file_path, format="mp4")
            sound = sound.set_frame_rate(8000).set_channels(1)
            wav_path = os.path.splitext(file_path)[0] + ".wav"
            sound.export(wav_path, format="wav")
        else:
            # Change the sample rate of the WAV file to 8000
            sound = AudioSegment.from_file(file_path, format="wav")
            sound = sound.set_frame_rate(8000).set_channels(1)
            file_path = os.path.splitext(file_path)[0] + "_8000.wav"
            sound.export(file_path, format="wav")

        # Open the WAV file
        wav_file = wave.open(file_path, 'rb')

        # Create a Vosk model and speech recognizer instance
        model_path = 'vosk-model-ru-0.42'
        model = vosk.Model(model_path)
        rec = vosk.KaldiRecognizer(model, wav_file.getframerate())

        # Create a TXT file with the same name as the input audio file
        txt_file = open(os.path.splitext(file_path)[0] + ".txt", "w", encoding="utf-8")

        # Read and recognize the audio file
        while True:
            data = wav_file.readframes(80000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                time = wav_file.tell() / wav_file.getframerate()  # Calculate time in seconds
                text_res = f"{time:.2f} s: {result['text']}\n"
                txt_file.write(text_res)
                print(text_res)
                self.ids.txt3.text = text_res

        # Get the final recognition result
        result = json.loads(rec.FinalResult())
        time = wav_file.getnframes() / wav_file.getframerate()  # Calculate time in seconds
        txt_file.write(text_res)
        self.ids.txt3.text = text_res

        # Close the files
        wav_file.close()
        txt_file.close()

    def start_speech_recognition_process(self):
        thread = threading.Thread(target=self.spech_recogn)
        thread.start()

    def save_3_text_to_file(self, *args):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.ids.txt3.text)
                # Если файл имеет расширение .docx, то сохраняем его в формате docx
                if file_path.endswith(".docx"):
                    document = Document()
                    document.add_paragraph(self.ids.txt3.text)
                    document.save(file_path)

    def open_33_file_dialog(self, *args):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
        if file_path:
            if file_path.endswith(".docx"):
                document = Document(file_path)
                self.ids.txt3.text = "\n".join([para.text for para in document.paragraphs])
            else:
                with open(file_path, 'r+', encoding='utf-8') as file:
                    self.ids.txt3.text = file.read()

    def increase_font_size3(self):
        self.ids.txt3.font_size += 2

    # метод для уменьшения размера шрифта
    def decrease_font_size3(self):
        self.ids.txt3.font_size -= 2

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
class Finddiff(MDIconButton):
    pass
class Removediff(MDIconButton):
    pass
class TxtFunctions():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secondtext = SecondText()
        self.voicetext = VoiceText()

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

