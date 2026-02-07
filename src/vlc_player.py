import tkinter as tk
from tkinter import ttk
import time
import vlc


class VLCPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None
        self.playlist = None
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self._track_finished)
        self.on_track_finished = None


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
    
    def _track_finished(self, event):
        if self.on_track_finished:
            self.on_track_finished()
        print("Song Finished")
        return
    
    def set_time(self, ms: int):
        self.player.set_time(ms)

    def get_time(self):
        return self.player.get_time()
    
    def get_length(self):
        return self.player.get_length()

    def volume_up(self):
        pass

    def volume_down(self):
        pass

    def volume_mute(self):
        pass
    

