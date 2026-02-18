import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from .playlist import Playlist
from .vlc_player import VLCPlayer
# from .styles import setup_styles

class Sidebar(ttk.Frame):
    def __init__(self, parent, playlist):
        super().__init__(parent)
        self.parent = parent
        self.playlist = playlist

        self.sidebar_tree = ttk.Treeview(self)
        self.sidebar_tree.pack(side="left", fill="both", expand=True)
        self.sidebar_tree.column("#0", width=200, stretch=False)
        self.sidebar_tree.heading("#0", text="")
        self.sidebar_tree.bind("<<TreeviewSelect>>", self.on_sidebar_click)


    def set_sidebar(self):
        library_id = self.sidebar_tree.insert("", "end", text="Library", values=("Library"))
        playlist_id = self.sidebar_tree.insert("", "end", text="Playlists", values=("Playlists"))
        
        self.sidebar_tree.insert(library_id, "end", text="Artists", values=("Artists", ))
        self.sidebar_tree.insert(library_id, "end", text="Albums", values=("Albums", ))
        self.sidebar_tree.insert(library_id, "end", text="Songs", values=("Songs", ))
        self.sidebar_tree.insert(library_id, "end", text="Favorites", values=("Favorites", ))

        self.sidebar_tree.insert(playlist_id, "end", text="All Playlists", values=("All Playlists"))

        self.sidebar_tree.item(library_id, open=True)
        self.sidebar_tree.item(playlist_id, open=True)


    def on_sidebar_click(self, event):
        selection = self.sidebar_tree.selection()
        if not selection:
            return
        self.selected_iid = selection[0]
        self.selected_view = self.sidebar_tree.item(self.selected_iid, "values")[0]
        self.event_generate("<<SidebarSelection>>")
        print("SIDEBAR CLICK:", self.selected_iid)
        print(self.selected_view)


class SecondarySidebar(ttk.Frame):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)
        self.populate(items)

    def populate(self, items):
        for i, item in enumerate(items):
            self.tree.insert("", "end", iid=str(i), text=item, values=(item, ))