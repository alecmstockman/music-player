from tkinter import ttk
from pathlib import Path
from .config import AUDIO_FILETYPES

class Playlist():
    def __init__(self, name, track_list):
        self.name = name
        self.track_list = track_list
        self.current_index = 0
        self.current_track = self.track_list[self.current_index]
        self.playlist_length = len(self.track_list)
        self.next_track = self.track_list[self.current_index + 1]

    def next(self):
        self.current_index += 1
        self.current_track = self.track_list[self.current_index]