#VoiceRecognition.py
import wave
import json
import vosk
from pydub import AudioSegment
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk, filedialog
import os

class VoiceToText(BoxLayout):
    def run_spech_recogn(self):
        voice_to_text = VoiceToText()
        voice_to_text.spech_recogn()

    def spech_recogn(self):
        print("Child process2")
        root = Tk()
        root.withdraw()
        file_path_recogn = filedialog.askopenfilename(
            filetypes=[('Video Files', '*.mp4'), ('MP3 Files', '*.mp3'), ('OGG Files', '*.ogg'), ('WAV Files', '*.wav'),
                       ('All Files', '*.*')]
        )

        audio_format = os.path.splitext(file_path_recogn)[1]
        if audio_format != ".wav":
            sound = AudioSegment.from_file(file_path_recogn, format=audio_format[1:])
            sound = sound.set_frame_rate(8000).set_channels(1)
            file_path_recogn = os.path.splitext(file_path_recogn)[0] + ".wav"
            sound.export(file_path_recogn, format="wav")
        elif file_path_recogn.endswith(".mp4"):
            sound = AudioSegment.from_file(file_path_recogn, format="mp4")
            sound = sound.set_frame_rate(8000).set_channels(1)
            wav_path = os.path.splitext(file_path_recogn)[0] + ".wav"
            sound.export(wav_path, format="wav")
        else:
            sound = AudioSegment.from_file(file_path_recogn, format="wav")
            sound = sound.set_frame_rate(8000).set_channels(1)
            file_path_recogn = os.path.splitext(file_path_recogn)[0] + "_8000.wav"
            sound.export(file_path_recogn, format="wav")

        wav_file = wave.open(file_path_recogn, 'rb')

        model_path = 'vosk-model-ru-0.42'
        model = vosk.Model(model_path)
        rec = vosk.KaldiRecognizer(model, wav_file.getframerate())

        txt_file = open(os.path.splitext(file_path_recogn)[0] + ".txt", "w", encoding="utf-8")

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

        result = json.loads(rec.FinalResult())
        time = wav_file.getnframes() / wav_file.getframerate()  # Calculate time in seconds
        txt_file.write(text_res)
        wav_file.close()
        txt_file.close()


    # def save_3_text_to_file(self, *args):
    #     file_path = filedialog.asksaveasfilename(defaultextension=".txt",
    #                                              filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
    #     if file_path:
    #         with open(file_path, 'w', encoding='utf-8') as file:
    #             file.write(self.ids.txt3.text)
    #             # Если файл имеет расширение .docx, то сохраняем его в формате docx
    #             if file_path.endswith(".docx"):
    #                 document = Document()
    #                 document.add_paragraph(self.ids.txt3.text)
    #                 document.save(file_path)
    #
    # def open_33_file_dialog(self, *args):
    #     root = Tk()
    #     root.withdraw()
    #     file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx")])
    #     if file_path:
    #         if file_path.endswith(".docx"):
    #             document = Document(file_path)
    #             self.ids.txt3.text = "\n".join([para.text for para in document.paragraphs])
    #         else:
    #             with open(file_path, 'r+', encoding='utf-8') as file:
    #                 self.ids.txt3.text = file.read()
    #
    # def increase_font_size3(self):
    #     self.ids.txt3.font_size += 2
    #
    # # метод для уменьшения размера шрифта
    # def decrease_font_size3(self):
    #     self.ids.txt3.font_size -= 2