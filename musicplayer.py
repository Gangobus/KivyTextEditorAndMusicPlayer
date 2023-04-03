import os
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from tkinter import Tk, filedialog
from kivy.core.audio import SoundLoader
from mutagen.mp3 import MP3
from kivy.clock import Clock
from kivy.uix.videoplayer import VideoPlayer
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


    def open_music_file_dialog(self, *args):
        root = Tk()
        root.withdraw()

        # показываем диалоговое окно выбора файла
        file_path = filedialog.askopenfilename(
            title="Выберите MP3-файл",  # заголовок диалогового окна
            filetypes=(("MP3 files", "*.mp3"),)  # расширения файлов, которые можно выбрать
        )
        if file_path:
            # загружаем выбранный файл в объект Sound
            sound = SoundLoader.load(file_path)#
            if sound:#
                # Получаем информацию о звуке
                self.current_sound = sound#
                self.file_path = file_path#
                audio = MP3(file_path)#

                duration = audio.info.length#
                file_size = os.path.getsize(file_path)#
                sample_rate = audio.info.sample_rate#


                musicfilename = f"{os.path.basename(file_path)}"#
                musicfileduration = f"{int(duration//3600):d}:{int(duration//60%60):02d}:{int(duration%60):02d}"#
                musicfilesize = f"{file_size / (1024*1024):.2f} МБ"#
                musicfilediscr = f"{sample_rate} Гц"#


                totalmusicfileduration = duration#
                totalhours, totalremainder = divmod(totalmusicfileduration, 3600)#
                totalminutes, totalseconds = divmod(totalremainder, 60)#
                totalformatted_time = f"{int(totalhours):d}:{int(totalminutes):02d}:{int(totalseconds):02d}"#

                bitrate = audio.info.bitrate / 1000  # kbps
                sample_rate = int(bitrate * 1000)  # Hz
                musicfilefrequency = f"{sample_rate} Гц"
                self.ids.mffreq.text = musicfilefrequency
                # update the playtime TextInput with the formatted time
                self.ids.totalduration.text = totalformatted_time

                self.ids.mfname.text = musicfilename#
                self.ids.mfdur.text = musicfileduration#
                self.ids.mfsize.text = musicfilesize#
                self.ids.mfdiscr.text = musicfilediscr#
                self.ids.mffreq.text = musicfilefrequency#



    def play_music(self, *args):
        if self.current_sound:#
            if self.last_played_pos:#
                # восстанавливаем проигрывание с сохраненной позиции
                self.current_sound.play()#
                self.current_sound.seek(self.last_played_pos)#
                self.last_played_pos = None#
                Clock.schedule_interval(self.update_playtime, 1)
            else:
                # начинаем проигрывание с начала
                self.current_sound.play()#
                Clock.schedule_interval(self.update_playtime, 1)



    def update_playtime(self, dt):
        if self.current_sound and self.current_sound.state == 'play':
            if self.current_sound and self.current_sound.state == 'play':
                # get the current playback time in seconds
                current_time = self.current_sound.get_pos() / 1

                # format the time as H:MM:SS
                hours, remainder = divmod(current_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                formatted_time = f"{int(hours):d}:{int(minutes):02d}:{int(seconds):02d}"

                # update the playtime TextInput with the formatted time
                self.ids.musictimenow.text = formatted_time
                # get the current playback position as a value between 0 and 1
                pos = self.current_sound.get_pos() / self.current_sound.length
                # set the value of the slider to the current position
                self.ids.seek_slider.value = pos
                print(pos, "update_playtime")
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