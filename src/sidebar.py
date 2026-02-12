import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from .playlist import Playlist
from .vlc_player import VLCPlayer
from .styles import setup_styles


class Sidebar(ttk.Frame):
    def __init__(self, parent, playlist):
        super().__init__(parent)
        self.parent = parent
        self.playlist = Playlist

        self.sidebar_tree = ttk.Treeview(self)
        self.sidebar_tree.pack(side="left", fill="both", expand=True)

        self.sidebar_tree.column("#0", width=200, stretch=False)
    
        self.sidebar_tree.heading("#0", text="")

    def set_sidebar(self):
        print("SIDEBAR SETUP")
        library_id = self.sidebar_tree.insert("", "end", text="Library")
        playlist_id = self.sidebar_tree.insert("", "end", text="Playlists")
        
        self.sidebar_tree.insert(library_id, "end", text="Artists")
        self.sidebar_tree.insert(library_id, "end", text="Albums")
        self.sidebar_tree.insert(library_id, "end", text="Songs")
        self.sidebar_tree.insert(library_id, "end", text="Favorites")

        self.sidebar_tree.insert(playlist_id, "end", text="All Playlists")

        self.sidebar_tree.item(library_id, open=True)
        self.sidebar_tree.item(playlist_id, open=True)

