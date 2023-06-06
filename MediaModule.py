#misucplayer.py
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk, filedialog
from mutagen.mp3 import MP3
import os
from kivy.core.audio import SoundLoader
import wave
from zipfile import BadZipFile
from pydub import AudioSegment

class Sound(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formatted_time = "00:00:00"
        self.file_path = None
        self.last_played_pos = None
        self.current_sound = None
        self.playing = False
        self.paused = False
        self.played_until_end = False
        self.video_player = None
        self.videobutton = None
        self.playtime_event = None
        self.previous_volume = 1
        self.play_pause_status = False
        self.slider_event = None
        self.playtime_event = None
        self.play_buffered_sound_event = None

    #метод для коректного вызова метода открытия аудиофайла
    def on_open_music_file_dialog(self, *args):
        Clock.schedule_once(self.open_music_file_dialog)
    #метод открытия аудиофайла через диалоговое окно
    def open_music_file_dialog(self, *args):
        try:
            root = Tk()
            root.withdraw()

            file_path_music = filedialog.askopenfilename(
                title="Select audio file",
                filetypes=(
                    ("MP3 files", "*.mp3"),
                    ("WAV files", "*.wav"),
                    ("OGG files", "*.ogg"),
                    ("FLAC files", "*.flac")
                )
            )

            if file_path_music:
                sound = SoundLoader.load(file_path_music)
                if sound:
                    self.current_sound = sound
                    self.file_path = file_path_music
                    duration = 0
                    file_size = os.path.getsize(file_path_music)
                    musicfilename = f"{os.path.basename(file_path_music)}"
                    musicfilesize = f"{file_size / (1024 * 1024):.2f} МБ"
                    if file_path_music.lower().endswith(".wav"):
                        with wave.open(file_path_music, "rb") as wav_file:
                            frames = wav_file.getnframes()
                            sample_rate = wav_file.getframerate()
                            duration = frames / float(sample_rate)
                            channels = wav_file.getnchannels()
                            bit_depth = wav_file.getsampwidth() * 8
                            musicfilediscr = f"{sample_rate} Гц, {channels} каналов, {bit_depth}-бит"
                    elif file_path_music.lower().endswith(".mp3"):
                        audio = MP3(file_path_music)
                        duration = audio.info.length
                        sample_rate = audio.info.sample_rate
                        musicfilediscr = f"{sample_rate} Гц"
                    elif file_path_music.lower().endswith(".ogg") or file_path_music.lower().endswith(".flac"):
                        audio = AudioSegment.from_file(file_path_music)
                        duration = len(audio) / 1000.0
                        sample_rate = audio.frame_rate
                        channels = audio.channels
                        bit_depth = audio.sample_width * 8
                        musicfilediscr = f"{sample_rate} Гц, {channels} каналов, {bit_depth}-бит"
                    musicfileduration = f"{int(duration // 3600):d}:{int(duration // 60 % 60):02d}:{int(duration % 60):02d}"
                    musicfilefrequency = f"{sample_rate} Гц"
                    self.ids.mfname.text = musicfilename
                    self.ids.mfdur.text = musicfileduration
                    self.ids.mfsize.text = musicfilesize
                    self.ids.mfdiscr.text = musicfilediscr
                    self.ids.mffreq.text = musicfilefrequency
                    self.ids.totalduration.text = musicfileduration
                    self.current_sound = SoundLoader.load(file_path_music)
                    self.current_sound.seek(0)
        except BadZipFile:
            pass
        except FileNotFoundError:
            pass
        except IOError:
            pass
        except PermissionError:
            pass
        except Exception as e:
            pass
    #воспроизведение/пауза аудио
    def playandpause(self):
        if self.play_pause_status == False:
            self.play_pause_status = True
            self.play_music()
        else:
            self.play_pause_status = False
            self.stop_music()

    #остановка воспроизведения
    def stop_audio(self):
        if self.play_pause_status == True:
            self.play_pause_status = False
            self.stop_music()
            self.last_played_pos = 0


    #запуск и подготовка к воспроизведению аудио
    def play_music(self, *args):
        if self.current_sound:
            if self.last_played_pos:
                self.current_sound.play()
                self.current_sound.seek(self.last_played_pos)
                self.last_played_pos = None
            else:
                self.current_sound.play()
                self.current_sound.stop()
                self.current_sound.seek(0)
            Clock.schedule_once(self.play_buffered_sound, 1)
        if self.current_sound == None:
            self.on_open_music_file_dialog()
            self.stop_music()

    #воспроизведение аудио
    def play_buffered_sound(self, dt):
        self.current_sound.play()
        self.update_slider(dt)
        self.playtime_event = Clock.schedule_interval(self.update_playtime, 0.2)
        self.slider_event = Clock.schedule_interval(self.update_slider, 0.1)

    #обновление положения слайдера перемотки
    def update_slider(self, dt):
        if self.current_sound and self.current_sound.state == 'play':
            current_pos = self.current_sound.get_pos()
            self.ids.seek_slider.value = current_pos / self.current_sound.length

    #обновлние отбображемого времени воспроизведения аудио
    def update_playtime(self, dt):
        if self.current_sound and self.current_sound.state == 'play':
            hours, remainder = divmod(self.current_sound.get_pos(), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.formatted_time = f"{int(hours):d}:{int(minutes):02d}:{int(seconds):02d}"
            self.ids.musictimenow.text = self.formatted_time
            self.set_formatted_time(self.formatted_time)

    # метод для передачи информации о текущем времени восрпоизведения
    def get_formatted_time(self):
        return self.formatted_time

    #метод для перемотки аудио перемешением слайдера
    def on_seek_slider_value(self, instance, value):
        if self.current_sound and self.current_sound.state == 'play':
            pos = value * self.current_sound.length
            self.current_sound.seek(pos)

    #метод остановки воспроизведения аудио
    def stop_music(self, *args):
        if self.current_sound:
            Clock.unschedule(self.playtime_event)
            Clock.unschedule(self.slider_event)
            self.last_played_pos = self.current_sound.get_pos()
            self.current_sound.stop()
            Clock.unschedule(self.playtime_event)
            Clock.unschedule(self.slider_event)
            Clock.unschedule(self.play_buffered_sound_event)
            Clock.unschedule(self.update_slider)
            Clock.unschedule(self.update_playtime)

    #метод перемотки аудио на 3 секунды вперёд
    def rewindplus(self):
        if self.current_sound:
            if self.current_sound and self.current_sound.state == 'play':
                pos = self.current_sound.get_pos() + 3
                self.current_sound.seek(pos)
            else:
                self.last_played_pos = self.last_played_pos + 3
        else:
            pass

    # метод перемотки аудио на 3 секунды назад
    def rewindminus(self):
        if self.current_sound:
            if self.current_sound and self.current_sound.state == 'play':
                pos = self.current_sound.get_pos() - 3
                pos = max(pos, 0)
                self.current_sound.seek(pos)
            else:
                self.last_played_pos = self.last_played_pos - 3
        else:
            pass

    # метод отключения звука воспроизведения
    def mute(self):
        if self.current_sound:
            self.current_sound.volume = 0

    # метод включения звука воспроизведения
    def unmute(self):
        if self.current_sound:
            self.current_sound.volume = self.previous_volume

        # метод для остановки воспроизведения и пермотки аудио на 3 сек назад
        def esc_press(self):
            if self.current_sound:
                self.playandpause()
                pos = self.current_sound.get_pos() - 3
                self.current_sound.seek(pos)
                self.last_played_pos = self.last_played_pos - 3

    #метод выбора видеофайла
    def play_video(self):
        if self.video_player is not None:
            self.stop_video()
            return
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[('Video Files', '*.mp4'), ('All Files', '*.*')]
        )
        self.video_player = VideoPlayer(source=file_path)
        self.ids.bta.add_widget(self.video_player)
        self.video_player.state = 'play'
        self.video_player.options = {'eos': 'stop'}

    #метод остановки воспроизведения видео
    def stop_video(self):
        self.on_stop()
        self.ids.bta.remove_widget(self.video_player)
        self.video_player = None

    # метод приостановки воспроизведения видео
    def on_pause(self):
        self.video_player.state = 'pause'

    # метод отключения видеоплеера
    def on_stop(self):
        self.video_player.state = 'stop'