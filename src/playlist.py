import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json
import vlc


class Playlist():
    def __init__(self, name, track_list):
        self.name = name
        self.track_list = track_list


class PlaylistManager():
    def __init__(self, library):
        self.library = library
        self.user_playlists = {"Playlist 1": None}

    def create_playlist(self, name, tracks=None):
        self.user_playlists[name] = Playlist(name, tracks or [])

    def save_playlists(self):
        path = Path("data/playlists.json")
        try: 
            with path.open("w", encoding="utf-8") as f:
                json.dump(self.user_playlists, f, indent=2)
        except Exception as e:
            print(f"Failed to save playlist: {e}")

    def load_playlist(self, name):
        path = Path("data/playlists.json")
        if not path.exists():
            self.user_playlists = {}
            return
        
        try: 
            with path.open("r", encoding="utf-8") as f:
                self.user_playlists = json.load(f)
        except Exception as e:
            print(f"Failed to load playlist: {e}")
            self.user_playlists = {}


class CreatePlaylistEntry(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()
        self.title("Create Playlist")
        self.result = None
        self.transient(parent)

        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="Playlist Name:").pack(anchor="w")

        self.entry = ttk.Entry(container, width=30)
        self.entry.pack(fill="x", pady=(4, 10))
        self.entry.focus()

        btn_row = ttk.Frame(container)
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text="Cancel", command=self.destroy).pack(side="right")
        ttk.Button(btn_row, text="Create", command=self.on_create).pack(side="right", padx=(0, 6))

        self.bind("<Return>", self.on_create)
        self.center_over_parent(parent)
        self.wait_visibility()
        self.deiconify()
        self.lift()
        self.grab_set()


    def center_over_parent(self, parent):
        root = parent.winfo_toplevel()
        self.update_idletasks()
        root.update_idletasks()

        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()
        root_w = root.winfo_width()
        root_h = root.winfo_height()

        win_w = self.winfo_reqwidth()
        win_h = self.winfo_reqheight()

        x = root_x + (root_w - win_w) // 2
        y = root_y - 100 + (root_h - win_h) // 2

        self.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.deiconify()
        self.lift()
        self.entry.focus_set()

    def on_create(self, event=None):
        name = self.entry.get().strip()
        if name:
            self.result = name
        self.destroy()

    