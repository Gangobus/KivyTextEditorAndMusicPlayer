from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from tkinter import Tk, filedialog
from mutagen.mp3 import MP3
import os

class TopMusicBar(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_path = None
        self.last_played_pos = None
        self.current_sound = None
        self.playing = False
        self.paused = False
        self.played_until_end = False
        self.video_player = None
        self.videobutton = None
        self.playtime_event = None

    def open_music_file_dialog(self, *args):
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Выберите MP3-файл",
            filetypes=(("MP3 files", "*.mp3"),)
        )
        if file_path:
            sound = SoundLoader.load(file_path)
            if sound:
                self.current_sound = sound
                self.file_path = file_path
                audio = MP3(file_path)

                duration = audio.info.length
                file_size = os.path.getsize(file_path)
                sample_rate = audio.info.sample_rate

                musicfilename = f"{os.path.basename(file_path)}"  #
                musicfileduration = f"{int(duration // 3600):d}:{int(duration // 60 % 60):02d}:{int(duration % 60):02d}"  #
                musicfilesize = f"{file_size / (1024 * 1024):.2f} МБ"  #
                musicfilediscr = f"{sample_rate} Гц"  #
                musicfileduration = f"{int(duration // 3600):d}:{int(duration // 60 % 60):02d}:{int(duration % 60):02d}"

                bitrate = audio.info.bitrate / 1000  # kbps
                sample_rate = int(bitrate * 1000)  # Hz
                musicfilefrequency = f"{sample_rate} Гц"

                self.ids.mfname.text = musicfilename
                self.ids.mfdur.text = musicfileduration
                self.ids.mfsize.text = musicfilesize
                self.ids.mfdiscr.text = musicfilediscr
                self.ids.mffreq.text = musicfilefrequency
                self.ids.totalduration.text = musicfileduration

                # Buffer the sound file
                self.current_sound = SoundLoader.load(file_path)
                self.current_sound.seek(0)

    def play_music(self, *args):
        if self.current_sound:
            # Восстанавливаем проигрывание с сохраненной позиции, если она есть
            if self.last_played_pos:
                self.current_sound.play()
                self.current_sound.seek(self.last_played_pos)
                self.last_played_pos = None
            # Начинаем проигрывание с начала, если сохраненной позиции нет
            else:
                self.current_sound.play()
                self.current_sound.stop()
                self.current_sound.seek(0)
            # Schedule the sound to play after it has been buffered
            Clock.schedule_once(self.play_buffered_sound, 0.001)


    def play_buffered_sound(self, dt):
        # Play the sound after it has been buffered
        self.current_sound.play()
        # Schedule the update_playtime function to run every second
        Clock.schedule_interval(self.update_playtime, 1)
        Clock.schedule_interval(self.update_slider, 0.5)
    def update_slider(self, dt):
        if self.current_sound and self.current_sound.state == 'play':
            self.ids.seek_slider.value = self.current_sound.get_pos() / self.current_sound.length
            print((self.current_sound.get_pos()), (self.current_sound.get_pos() / self.current_sound.length))
    def update_playtime(self, dt):
        if self.current_sound and self.current_sound.state == 'play':

            # format the time as H:MM:SS
            hours, remainder = divmod(self.current_sound.get_pos(), 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{int(hours):d}:{int(minutes):02d}:{int(seconds):02d}"

            # update the playtime TextInput with the formatted time
            self.ids.musictimenow.text = formatted_time

    def on_seek_slider_value(self, instance, value):
        # Проверяем, есть ли звуковой файл и проигрывается ли он
        if self.current_sound and self.current_sound.state == 'play':
            # Вычисляем новую позицию воспроизведения, исходя из значения слайдера
            pos = self.current_sound.length * value
            # Устанавливаем новую позицию воспроизведения
            self.current_sound.seek(pos)
            print(pos, "on_seek_slider_value")
    def stop_music(self, *args):
        # останавливаем проигрывание звука (если он есть)
        if self.current_sound:
            self.last_played_pos = self.current_sound.get_pos()
            self.current_sound.stop()

    def rewindplus(self):
        # Проверяем, есть ли звуковой файл и проигрывается ли он
        if self.current_sound and self.current_sound.state == 'play':
            # Получаем текущую позицию воспроизведения и добавляем 10 секунд
            pos = self.current_sound.get_pos() + 10
            # Ограничиваем позицию, чтобы не выходила за границы длительности звукового файла
            pos = min(pos, self.current_sound.length)
            # Устанавливаем новую позицию воспроизведения
            self.current_sound.seek(pos)
        else:
            self.last_played_pos = self.last_played_pos + 10

    def rewindminus(self):
        # Проверяем, есть ли звуковой файл и проигрывается ли он
        if self.current_sound and self.current_sound.state == 'play':
            # Получаем текущую позицию воспроизведения и вычитаем 10 секунд
            pos = self.current_sound.get_pos() - 10
            # Ограничиваем позицию, чтобы не выходила за границы звукового файла
            pos = max(pos, 0)
            # Устанавливаем новую позицию воспроизведения
            self.current_sound.seek(pos)
        else:
            self.last_played_pos = self.last_played_pos - 10

    def play_video(self):
        # если видеоплеер уже создан, закрываем его
        if self.video_player is not None:
            self.stop_video()
            return

        # вызов диалогового окна для выбора файла
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[('Video Files', '*.mp4'), ('All Files', '*.*')]
        )

        # создание виджета VideoPlayer и воспроизведение выбранного видео
        self.video_player = VideoPlayer(source=file_path)
        self.ids.bta.add_widget(self.video_player)
        self.video_player.state = 'play'

    def stop_video(self):
        self.ids.bta.remove_widget(self.video_player)
        self.video_player = None
    def on_pause(self):
        self.video_player.state = 'pause'

    def on_stop(self):
        self.video_player.state = 'stop'