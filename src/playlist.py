import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json
import uuid
import vlc


class Playlist():
    def __init__(self, name, track_list=None, song_id=None):
        self.id = song_id
        self.name = name
        self.track_list = track_list


class PlaylistManager():
    def __init__(self, library):
        self.library = library
        self.user_playlists = {}
        self.id = uuid.uuid4()

    def create_playlist(self, name, tracks=None):
        if tracks == None:
            playlist = Playlist(name, [])
        else:
            playlist = Playlist(name, tracks)
        print(f"CREATE PLAYLIST: {playlist}")
        playlist.id = str(uuid.uuid4())
        self.user_playlists[playlist.id] = playlist
        self.save_playlists()
        return playlist

    def save_playlists(self):
        user_playlists = {}
        for key, value in self.user_playlists.items():
            track_list = []
            for track in value.track_list:
                track_list.append(str(track))
            user_playlists[key] = {"name": value.name, "tracks": track_list, "id": key}
        path = Path("data/playlists.json")
        try: 
            with path.open("w", encoding="utf-8") as f:
                json.dump(user_playlists, f, indent=2)
        except Exception as e:
            print(f"Failed to save playlist: {e}")

    def load_playlist(self):
        user_playlists = {}
        path = Path("data/playlists.json")

        if not path.exists():
            self.user_playlists = {}
            return
        try: 
            with path.open("r", encoding="utf-8") as f:
                user_playlists = json.load(f)
        except Exception as e:
            print(f"Failed to load playlist: {e}")
            self.user_playlists = {}

        for key, value in user_playlists.items():
            path_list = []
            track_list = value["tracks"]
            for track in track_list:
                path_list.append(Path(track))
            self.user_playlists[key] = Playlist(value["name"], path_list, key)
    
    def add_to_user_playlist(self, key, name, track):
        print("\nPLAYLIST: - ADD TO USER PLAYLIST")
        playlist = self.user_playlists[key]
        playlist.track_list.append(track)
        self.save_playlists()

    def delete_user_playlist(self, playlist_id):
        remaining_user_playlists = {}
        for key, playlist in self.user_playlists.items():
            if key != playlist_id:
                remaining_user_playlists[key] = playlist

        self.user_playlists = remaining_user_playlists
        self.save_playlists()


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

    