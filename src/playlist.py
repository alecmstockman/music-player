import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json
import uuid
from dataclasses import dataclass
from .config import AUDIO_FILETYPES
from src.metadata import load_track_metadata

    
ROOT = Path(__file__).resolve().parent.parent
MUSIC = Path(f"{ROOT}/Music/")
LIBRARY_JSON_PATH = Path(ROOT/"data/library.json")
LIBRARY_JSON_PATH.parent.mkdir(exist_ok=True)

# class Track():
#     def __init__(self, filepath, track_id, title, artist, album, length, composer, copyright, albumartist, conductor, discnumber, tracknumber, genre, date, sample_rate, bit_rate, channels, codec, play_count, favorite, **metadata):
#         self.filepath = metadata["filepath"]
#         self.track_id = metadata["track_id"]
#         self.title = metadata["title"]
#         self.artist = metadata["artist"]
#         self.album = metadata["album"]
#         self.length = metadata["length"]

#         self.composer = metadata["composer"]
#         self.copyright = metadata["copyright"]
#         self.albumartist = metadata["albumartist"]
#         self.conductor = metadata["conductor"]
#         self.discnumber = metadata["discnumber"]
#         self.tracknumber = metadata["tracknumber"]
#         self.genre = metadata["genre"]
#         self.date = metadata["date"]

#         self.sample_rate = metadata["sample_rate"]
#         self.bit_rate = metadata["bit_rate"]
#         self.channels = metadata["channels"]
#         self.codec = metadata["codec"]

#         self.play_count = 0
#         self.favorite = False

#     def __repr__(self):
#         return (f"TITLE: {self.title}, ARTIST: {self.artist}, ALBUM: {self.album}, ID: {self.track_id}")
    
#     def __str__(self):
#         return (f"TITLE: {self.title}, ARTIST: {self.artist}, ALBUM: {self.album}, ID: {self.track_id}")
    
#     def __eq__(self, other):
#         return self.filepath == other.filepath

class Track:
    def __init__(self, track_id=None, title=None, artist=None, album=None, length=None, play_count=None, favorite=None, **metadata):
        self.track_id = track_id
        self.title = title
        self.artist = artist
        self.album = album
        self.length = length

        self.play_count = play_count
        self.favorite = favorite

        for key, value in metadata.items():
            setattr(self, key, value)


    def __repr__(self):
        return (f"TITLE: {self.title}, ARTIST: {self.artist}, ALBUM: {self.album}, ID: {self.track_id}")
    
    def __str__(self):
        return (f"TITLE: {self.title}, ARTIST: {self.artist}, ALBUM: {self.album}, ID: {self.track_id}")
    
    def __eq__(self, other):
        return self.filepath == other.filepath

class Library():
    def __init__(self):
        self.name = "Library"
        self.tracks = {}

    def __str__(self):
        return str(self.tracks)

    def create_library(self):
        LIBRARY_JSON_PATH.parent.mkdir(exist_ok=True)

        filename_list = [filename for filename in MUSIC.rglob('*') if filename.suffix in AUDIO_FILETYPES]

        all_tracks = []
        for name in filename_list:
            track_data = load_track_metadata(name)
            track = Track(**track_data)
            all_tracks.append(track)

        for track in all_tracks:
            self.tracks[track.track_id] = track

        self.save_library()

    def load_library(self):
        if not LIBRARY_JSON_PATH.exists():
            print("Library json file not found, creating new library")
            self.create_library()
            return
        
        try: 
            with LIBRARY_JSON_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)

                for track_id, track_data in data.items():
                    track = Track(**track_data)
                    self.tracks[track_id] = track

        except Exception as e:
            print(f"Failed to load library: {e}")

    def add_track(self, track):
        self.tracks[track.track_id] = track
 
    def remove_track(self, track):
        pass

    def get_track(self, track_id):
        return self.tracks[track_id]

    def save_library(self):
        print("save library")
        library = {}
        for track in self.tracks.values():
            library[track.track_id] = {
                key: str(value) if key == "filepath" else value
                for key, value in vars(track).items()
            }

        try: 
            with LIBRARY_JSON_PATH.open("w", encoding="utf-8") as f:
                json.dump(library, f , indent=2)
        except Exception as e:
            print(f"Failed to save library: {e}")


class Playlist():
    def __init__(self, name, track_id_list=None, song_id=None):
        self.id = song_id if song_id is not None else uuid.uuid4()
        self.name = name
        self.track_id_list = track_id_list

    def __repr__(self):
        return f"PLAYLIST NAME: {self.name}, ID: {self.id}"
    
    def __str__(self):
        return f"PLAYLIST NAME: {self.name}, ID: {self.id}"

class PlaylistManager():
    def __init__(self, library):
        self.library = library
        self.library_playlist = None
        self.user_playlists = {}
        self.id = uuid.uuid4()

    def create_library_playlist(self):
        library_track_list = []
        for item in self.library.tracks.keys():
            library_track_list.append(item)
        self.library_playlist = Playlist("Library Playlist", library_track_list)

    def create_playlist(self, name, tracks=None):
        if tracks == None:
            playlist = Playlist(name, [])
        else:
            playlist = Playlist(name, tracks)
        playlist.id = str(uuid.uuid4())
        self.user_playlists[playlist.id] = playlist
        self.save_playlists()
        return playlist

    def save_playlists(self):
        user_playlists = {}
        for key, value in self.user_playlists.items():
            track_list = []
            for track in value.track_id_list:
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
        playlist = self.user_playlists[key]
        playlist.track_id_list.append(track)
        self.save_playlists()

    def update_user_playlist(self, playlist_id):
        playlist = self.user_playlists[playlist_id]
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

    