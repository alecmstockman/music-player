import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from .playlist import Playlist
from .vlc_player import VLCPlayer
import json
# from .styles import setup_styles

class Sidebar(ttk.Frame):
    def __init__(self, parent, playlist, playlist_manager):
        super().__init__(parent)
        self.parent = parent
        self.playlist = playlist
        self.playlist_manager = playlist_manager
        self.selected_view = None
        self.playlist_id = None

        self.sidebar_tree = ttk.Treeview(self)
        self.sidebar_tree.pack(side="left", fill="both", expand=True)
        self.sidebar_tree.column("#0", width=200, stretch=False)
        self.sidebar_tree.heading("#0", text="")
        self.sidebar_tree.bind("<<TreeviewSelect>>", self.on_sidebar_click)


    def set_sidebar(self):
        library_id = self.sidebar_tree.insert("", "end", text="Library", values=("Library"))
        self.playlist_id = self.sidebar_tree.insert("", "end", text="Playlists", values=("Playlists"))
        playlists = self.playlist_manager.user_playlists
        
        self.sidebar_tree.insert(library_id, "end", text="Artists", values=("Artists", ))
        self.sidebar_tree.insert(library_id, "end", text="Albums", values=("Albums", ))
        self.sidebar_tree.insert(library_id, "end", text="Songs", values=("Songs", ))
        self.sidebar_tree.insert(library_id, "end", text="Favorites", values=("Favorites", ))

        self.sidebar_tree.insert(self.playlist_id, "end", text="All Playlists", values=("All Playlists"))

        self.sidebar_tree.item(library_id, open=True)
        self.sidebar_tree.item(self.playlist_id, open=True)

        for item in self.playlist_manager.user_playlists.keys():
            playlist = self.playlist_manager.user_playlists[item]
            playlist_name = playlist.split(",")[0]
            self.sidebar_tree.insert(self.playlist_id, "end", text=f"- {playlist_name}")

    def on_sidebar_click(self, event):
        selection = self.sidebar_tree.selection()
        if not selection:
            return
        self.selected_iid = selection[0]
        self.selected_view = self.sidebar_tree.item(self.selected_iid, "values")[0]
        self.event_generate("<<SidebarSelection>>")
        print("SIDEBAR CLICK:", self.selected_iid)
        print(self.selected_view)

    def add_user_playlist(self, playlist):
        print("ADD USER PLAYLIST")
        if not playlist:
            return
        
        if not self.playlist_id:
            print("Playlist parent not initialized")
            return
        
        self.sidebar_tree.insert(self.playlist_id, "end", text=f"- {playlist.name}")
        
    # def delete_user_playlist(self, playlist):
    #     pass

    # def save_user_playlist(self, playlist):
    #     path = Path("data/playlists.json")
    #     item = {str(playlist.name): [], }
    #     try: 
    #         with path.open("w", encoding="utf-8") as f:
    #             json.dump(item, f, indent=2)
    #     except Exception as e:
    #         print(f"Failed to save favorites: {e}")

    # def load_user_playlist(self):
    #     path = Path("data/playlists.json")


class SecondarySidebar(ttk.Frame):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)
        self.populate(items)
        self.selected_view = None
        self.tree.bind("<<TreeviewSelect>>", self.on_secondary_sidebar_click)

    def populate(self, items):
        for i, item in enumerate(items):
            self.tree.insert("", "end", iid=str(i), text=item, values=(item, ))

    def on_secondary_sidebar_click(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_iid = selection[0]
        self.selected_view = self.tree.item(self.selected_iid, "values")[0]
        self.event_generate("<<SecondarySidebarSelection>>")
        print("SECONDARY SIDEBAR CLICK:", self.selected_iid)
        print(f"on_secondary_sidebar_click, selected_view: {self.selected_view}")
