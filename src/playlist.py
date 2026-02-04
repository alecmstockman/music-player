from tkinter import ttk
from pathlib import Path
from .config import AUDIO_FILETYPES

# track_list_names = [song.name for song in track_list]
# album_names = [album.name for album in album_dir_list]

class Playlist():
    def __init__(self, name, track_list):
        self.name = name
        self.track_list = track_list
        self.current_index = 0



