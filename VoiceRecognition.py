import os
import wave
import json
import vosk
from pydub import AudioSegment
from tkinter import Tk, filedialog

#открытие диалогового окна выбора файла
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    filetypes=[('Video Files', '*.mp4'), ('MP3 Files', '*.mp3'), ('OGG Files', '*.ogg'), ('WAV Files', '*.wav'), ('All Files', '*.*')]
)

#конвертация файлво в wav формат с частотой дискретизации 8000
audio_format = os.path.splitext(file_path)[1]
if audio_format != ".wav":
    sound = AudioSegment.from_file(file_path, format=audio_format[1:])
    sound = sound.set_frame_rate(8000).set_channels(1)
    file_path = os.path.splitext(file_path)[0] + ".wav"
    sound.export(file_path, format="wav")
elif file_path.endswith(".mp4"):
    sound = AudioSegment.from_file(file_path, format="mp4")
    sound = sound.set_frame_rate(8000).set_channels(1)
    wav_path = os.path.splitext(file_path)[0] + ".wav"
    sound.export(wav_path, format="wav")
else:

    sound = AudioSegment.from_file(file_path, format="wav")
    sound = sound.set_frame_rate(8000).set_channels(1)
    file_path = os.path.splitext(file_path)[0] + "_8000.wav"
    sound.export(file_path, format="wav")

# открытие полученного wav
wav_file = wave.open(file_path, 'rb')

# создание и развертывание языковой модели
model_path = 'vosk-model-ru-0.42'
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, wav_file.getframerate())

# создание txt файла
txt_file = open(os.path.splitext(file_path)[0] + ".txt", "w", encoding="utf-8")

# чтение и распознование файла покускам = 80000 кадров
while True:
    data = wav_file.readframes(80000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        time = wav_file.tell() / wav_file.getframerate()  # Calculate time in seconds
        txt_file.write(f"{time:.2f} s: {result['text']}\n")
        print(f"{time:.2f} s: {result['text']}\n")

# получение и сохранение резултата
result = json.loads(rec.FinalResult())
time = wav_file.getnframes() / wav_file.getframerate()  # Calculate time in seconds
txt_file.write(f"{time:.2f} s: {result['text']}\n")

#закрытие файлов
wav_file.close()
txt_file.close()
