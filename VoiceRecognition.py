import os
import wave
import json
import vosk
from pydub import AudioSegment
from tkinter import Tk, filedialog

# Open a file dialog box to select the input audio file
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    filetypes=[('Video Files', '*.mp4'), ('MP3 Files', '*.mp3'), ('OGG Files', '*.ogg'), ('WAV Files', '*.wav'), ('All Files', '*.*')]
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
        txt_file.write(f"{time:.2f} s: {result['text']}\n")
        print(f"{time:.2f} s: {result['text']}\n")

# Get the final recognition result
result = json.loads(rec.FinalResult())
time = wav_file.getnframes() / wav_file.getframerate()  # Calculate time in seconds
txt_file.write(f"{time:.2f} s: {result['text']}\n")

# Close the files
wav_file.close()
txt_file.close()
