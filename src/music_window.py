import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.playlist import Playlist
from src.vlc_player import VLCPlayer
from src.styles import setup_styles


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, player, Playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = Playlist

        self.playlist_tree = ttk.Treeview(self, columns=("Title", "Time"))
        self.playlist_tree.pack()

        self.playlist_tree.heading("Age", text="Age")
        self.playlist_tree.heading("Time", text="Time")
        self.playlist_tree.column("Track", anchor="w")

        self.playlist_tree.pack(side="left", fill="both")