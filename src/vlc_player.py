import tkinter as tk
from tkinter import ttk
import time
import vlc


class VLCPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None
        self.event_manager = self.player.event_manager()

    def load(self, filepath: str):
        self.media = self.instance.media_new(filepath)
        self.player.set_media(self.media)

    def play(self):
        if self.media is not None:
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_playing(self) -> bool:
        return bool(self.player.is_playing())
    
    def set_time(self, ms: int):
        self.player.set_time(ms)
    
    def get_time(self):
        return self.player.get_time()
    
    def get_length(self):
        return self.player.get_length()
    
    def set_volume(self, volume: int):
        self.player.audio_set_volume(volume)

    def volume_mute(self):
        pass