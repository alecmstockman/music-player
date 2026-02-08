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

        self.playlist_tree = ttk.Treeview(self, columns=("Play Status", "Track", "Time", "Artist", "Album", "Blank"), show="headings")
        self.playlist_tree.pack(side="left", fill="both", expand=True)
        
        self.playlist_tree.column("Play Status", anchor="w", width=50, stretch=False)
        self.playlist_tree.column("Track", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Time", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Artist", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Album", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Blank", anchor="w", width=200, stretch=True)

        self.playlist_tree.heading("Play Status", text="  ")
        self.playlist_tree.heading("Track", text="Title")
        self.playlist_tree.heading("Time", text="Time")
        self.playlist_tree.heading("Artist", text="Artist")
        self.playlist_tree.heading("Album", text="Album")
        self.playlist_tree.heading("Blank", text="")
        

        # self.playlist_tree.pack(side="left", fill="both")