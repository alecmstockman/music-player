from tkinter import ttk
from pathlib import Path
from .config import AUDIO_FILETYPES

class Playlist():
    def __init__(self, name, track_list):
        self.name = name
        self.track_list = track_list
        self.current_index = 0
        self.playlist_length = len(self.track_list)

    # def next(self):
    #     if self.current_index < len(self.track_list) -1:
    #         self.current_index += 1
    #     return self.current_index

    # def previous(self):
    #     if self.current_index > 0:
    #         self.current_index -=1
    #     return self.current_index
    

