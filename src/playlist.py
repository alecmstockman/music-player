from tkinter import ttk
from pathlib import Path

class Playlist():
    def __init__(self, name, track_list):
        self.name = name
        self.track_list = track_list
        