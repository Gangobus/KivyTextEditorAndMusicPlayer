from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk, filedialog
from mutagen.mp3 import MP3
import os
from kivy.core.audio import SoundLoader
import keyboard
import wave
import soundfile as sf

class TopMusicBar(BoxLayout):
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

        keyboard.add_hotkey("F3", self.rewindplus)
        keyboard.add_hotkey("F2", self.rewindminus)
        keyboard.add_hotkey("F4", self.playandpause)

    def on_open_music_file_dialog(self, *args):
        Clock.schedule_once(self.open_music_file_dialog)
        print("on_open_music_file_dialog")

    def open_music_file_dialog(self, *args):
        print("open_music_file_dialog")
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

                elif file_path_music.lower().endswith(".ogg"):
                    audio, sample_rate = sf.read(file_path_music)
                    duration = len(audio) / float(sample_rate)
                    channels = audio.shape[1]
                    bit_depth = audio.dtype.itemsize * 8
                    musicfilediscr = f"{sample_rate} Гц, {channels} каналов, {bit_depth}-бит"

                elif file_path_music.lower().endswith(".flac"):
                    audio, sample_rate = sf.read(file_path_music)
                    duration = len(audio) / float(sample_rate)
                    channels = audio.shape[1]
                    bit_depth = audio.dtype.itemsize * 8
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

    def playandpause(self):
        print("playandpause")
        if self.play_pause_status == False:
            self.play_pause_status = True
            self.play_music()
        else:
            self.play_pause_status = False
            self.stop_music()

    def rebind_keyboardhotkeys(self, *args):
        print("rebind_keyboardhotkeys")
        keyboard.add_hotkey("F3", self.rewindplus)
        keyboard.add_hotkey("F2", self.rewindminus)
        keyboard.add_hotkey("F4", self.playandpause)
        keyboard.add_hotkey("Esc", self.esc_press)

    def esc_press(self):
        print("esc_press")
        self.stop_music()
        if self.current_sound:
            if self.current_sound and self.current_sound.state == 'play':
                pos = self.current_sound.get_pos() - 3
                pos = max(pos, 0)
                self.current_sound.seek(pos)
            else:
                self.last_played_pos = self.last_played_pos - 3
        else:
            pass

    def play_music(self, *args):
        print("play_music")
        if self.current_sound:
            if self.last_played_pos:
                self.current_sound.play()
                self.current_sound.seek(self.last_played_pos)
                self.last_played_pos = None
            else:
                self.current_sound.play()
                self.current_sound.stop()
                self.current_sound.seek(0)

            Clock.schedule_once(self.play_buffered_sound, 0.5)

    def play_buffered_sound(self, dt):
        print("play_buffered_sound")
        self.current_sound.play()
        self.update_slider(dt)
        self.playtime_event = Clock.schedule_interval(self.update_playtime, 0.2)
        self.slider_event = Clock.schedule_interval(self.update_slider, 0.1)


    def update_slider(self, dt):
        print("update_slider")
        if self.current_sound and self.current_sound.state == 'play':
            current_pos = self.current_sound.get_pos()
            self.ids.seek_slider.value = current_pos / self.current_sound.length

    def update_playtime(self, dt):
        print("update_playtime")
        if self.current_sound and self.current_sound.state == 'play':
            hours, remainder = divmod(self.current_sound.get_pos(), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.formatted_time = f"{int(hours):d}:{int(minutes):02d}:{int(seconds):02d}"
            self.ids.musictimenow.text = self.formatted_time
            self.set_formatted_time(self.formatted_time)

    def get_formatted_time(self):
        print("get_formatted_time")
        return self.formatted_time


    def on_seek_slider_value(self, instance, value):
        print("on_seek_slider_value")
        if self.current_sound and self.current_sound.state == 'play':
            pos = value * self.current_sound.length
            self.current_sound.seek(pos)

    def stop_music(self, *args):
        print("stop_music")
        if self.current_sound:
            Clock.unschedule(self.playtime_event)
            Clock.unschedule(self.slider_event)
            self.last_played_pos = self.current_sound.get_pos()
            self.current_sound.stop()

    def rewindplus(self):
        print("rewindplus")
        if self.current_sound:
            if self.current_sound and self.current_sound.state == 'play':
                pos = self.current_sound.get_pos() + 10
                self.current_sound.seek(pos)
            else:
                self.last_played_pos = self.last_played_pos + 10
        else:
            pass

    def rewindminus(self):
        print("rewindminus")
        if self.current_sound:
            if self.current_sound and self.current_sound.state == 'play':
                pos = self.current_sound.get_pos() - 10
                pos = max(pos, 0)
                self.current_sound.seek(pos)
            else:
                self.last_played_pos = self.last_played_pos - 10
        else:
            pass
    def mute(self):
        print("mute")
        if self.current_sound:
            self.current_sound.volume = 0

    def unmute(self):
        print("unmute")
        if self.current_sound:
            self.current_sound.volume = self.previous_volume

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

    def stop_video(self):
        self.ids.bta.remove_widget(self.video_player)
        self.video_player = None
    def on_pause(self):
        self.video_player.state = 'pause'

    def on_stop(self):
        self.video_player.state = 'stop'

