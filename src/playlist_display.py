import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.playlist import Playlist, PlaylistManager, CreatePlaylistEntry
from src.vlc_player import VLCPlayer
import json
# from src.styles import setup_styles
from src.config import AUDIO_FILETYPES


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, player, playlist, playlist_manager):
        super().__init__(parent)
        self.player = player
        self.playlist = playlist
        self.playlist_manager = playlist_manager
        
        self.popup_menu = tk.Menu(self, tearoff=False)
        self.playlist_submenu = tk.Menu(self.popup_menu, tearoff=False)
        # self.menu_iid = None
        self.menu_iid = None
        self.favorites = {}
        self.load_favorites()
        self._last_playlist_created = None

        self.playlist_tree = ttk.Treeview(
            self, 
            columns=("filepath", "index", "play status", "Track", "Menu", "Time", "Artist", "Album", "favorite", "Filetype", "Blank"), 
            show="headings"
        )
        self.playlist_tree.pack(side="left", fill="both", expand=True)
        
        self.playlist_tree.column("filepath", width=0, stretch=False)
        self.playlist_tree.column("index", width=0, stretch=False)
        self.playlist_tree.column("play status", anchor="w", width=40, stretch=False)
        self.playlist_tree.column("Track", anchor="w", width=400, stretch=False)
        self.playlist_tree.column("Menu", anchor="e", width=20, stretch=False)
        self.playlist_tree.column("Time", anchor="e", width=60, stretch=False)
        self.playlist_tree.column("Artist", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Album", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Filetype", anchor="e", width=100, stretch=False)
        self.playlist_tree.column("favorite", anchor="e", width=40, stretch=False)
        self.playlist_tree.column("Blank", anchor="w", width=200, stretch=True)
        
        self.playlist_tree.heading("filepath")
        self.playlist_tree.heading("index")
        self.playlist_tree.heading("play status", text="  ")
        self.playlist_tree.heading("Track", text="Title")
        self.playlist_tree.heading("Menu", text="···")
        self.playlist_tree.heading("Time", text="Time")
        self.playlist_tree.heading("Artist", text="Artist")
        self.playlist_tree.heading("Album", text="Album")
        self.playlist_tree.heading("favorite", text="  ")
        self.playlist_tree.heading("Filetype", text="Filetype")
        self.playlist_tree.heading("Blank", text="")

        self.playlist_tree.bind("<Button-1>", self.on_tree_click)

        self.popup_menu.add_command(label="Play", command=self._on_menu_play)
        self.popup_menu.add_command(label="Previous", command=self._on_menu_previous_track)
        self.popup_menu.add_command(label="Next", command=self._on_menu_next_track)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Create Playlist", command=self._on_menu_create_playlist)
        self.popup_menu.add_cascade(label="Add to Playlist", menu=self.playlist_submenu)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Favorite", command=self._on_menu_update_favorite)
        self.popup_menu.add_command(label="Remove Favorite", command=self._on_menu_update_favorite)

        self.playlist_tree.bind("<<TreeviewSelect>>", self.on_tree_click)


    def set_playlist(self, playlist):
        self.playlist = playlist
        self.clear_playlist()
        if not playlist or not hasattr(playlist, "track_list"):
            print("No playlist or invalid playlist object")
            return
        index = 0
        even = True
        for track in self.playlist.track_list:
            if not track or not track.exists():
                print(f"Skipping invalid track: {track}")
                continue
            media = self.player.instance.media_new(track)
            media.parse()

            filepath = self.playlist.track_list[index]
            title = media.get_meta(vlc.Meta.Title)
            artist = media.get_meta(vlc.Meta.Artist)
            album = media.get_meta(vlc.Meta.Album)
            total_s = media.get_duration() // 1000
            total_str = f"{total_s//60:d}:{total_s%60:02d}"
            filetype = track.suffix[1:]

            self.playlist_tree.tag_configure("even", background="darkblue")
            self.playlist_tree.tag_configure("odd", background="black")

            is_fav = self.favorites.get(str(filepath), False)
            star = " ★ " if is_fav else " ☆ "

            if track.suffix in AUDIO_FILETYPES:
                track_index = index
                if even is True:
                    self.playlist_tree.insert(
                        "", "end",
                        iid=str(track_index),
                        values=(filepath, f"{track_index}", "", f"{title}", "···", f"{total_str}", f"{artist}", f"{album}", f"{star}", f"{filetype}"),
                        tags="even" 
                    )
                    even = False
                else:
                    self.playlist_tree.insert(
                        "", "end",
                        iid=str(track_index), 
                        values=(filepath, f"{track_index}", "", f"{title}", "···", f"{total_str}", f"{artist}", f"{album}", f"{star}", f"{filetype}"),
                        tags="odd" 
                    )
                    even = True
                index += 1

    def clear_playlist(self):
        for iid in self.playlist_tree.get_children():
            self.playlist_tree.delete(iid)

    def get_selected_tracks(self):
        print("GET SELECTED TRACK")
        print(f"Playlist Display: playlist {self.playlist.name}")
        selection = self.playlist_tree.selection()

        if not selection:
            print("playlist_display: get_selected_tracks, no selection")
            return None
        
        selected_iid = self.playlist_tree.item(selection[0])
        values = selected_iid["values"]
        return {
            "filepath": values[0],
            "index": values[1],
            "play status": values[2],
            "title": values[3],
            "length": values[4],
            "artist": values[5], 
            "album": values[6],
            "filetype": values[7]
        }
    
    def clear_play_status(self):
        for iid in self.playlist_tree.get_children():
            if iid is None:
                return
            self.playlist_tree.set(iid, column="play status", value="")

    def remove_play_status_icon(self, index):
        if index is None:
            print("playlist_display: remove_play_status_icon, index is None")
            return
        iid = index
        self.playlist_tree.set(iid, column="play status", value="   ")

    def play_status_icon_playing(self, index):
        if not self.playlist_tree.get_children():
            return
        if index is None:
            print("playlist_display: play_status_icon_playing, index is None")
            return
        iid = index
        self.playlist_tree.set(iid, column="play status", value="  🔊")

    def play_status_icon_paused(self, index):
        if not self.playlist_tree.get_children():
            return
        if index is None:
            print("playlist_display: play_status_icon_paused, index is None")
            return
        iid = index
        self.playlist_tree.set(iid, column="play status", value="  🔈")


    def on_tree_click(self, event):
        row_id = self.playlist_tree.identify_row(event.y)
        col_id = self.playlist_tree.identify_column(event.x)

        if not row_id:
            return

        self.playlist_tree.selection_set(row_id)
        self.playlist_tree.event_generate("<<TreeviewSelect>>")

        self.menu_iid = row_id
        if col_id == "#5":
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        elif col_id == "#9":
            self._update_favorite(row_id)

    def _on_menu_play(self):
        self.clear_play_status()
        self.controls.play_index = int(self.menu_iid)
        index = self.controls.play_order[self.controls.play_index]
        track = self.playlist.track_list[index]
        self.player.load(track)
        self.player.play()
        self.play_status_icon_playing(index)

    def _on_menu_previous_track(self):
        self.clear_play_status()
        self.controls.play_index = int(self.menu_iid)
        self.controls.previous_track()        

    def _on_menu_next_track(self):
        self.clear_play_status()
        self.controls.play_index = int(self.menu_iid)
        self.controls.next_track()

    def _on_menu_create_playlist(self):
        dialog = CreatePlaylistEntry(self)
        self.wait_window(dialog)
        playlist_name = dialog.result

        if not playlist_name:
            return

        playlist = self.playlist_manager.create_playlist(playlist_name)

        self._last_playlist_created = playlist
        self.event_generate("<<PlaylistCreated>>")

    def _set_popup_playlist_list(self):
        self.playlist_submenu.delete(0, "end")
        for key, value in self.playlist_manager.user_playlists.items():
            self.playlist_submenu.add_command( 
                label=f"{value.name}", 
                command=lambda k=key, n=value.name: 
                    self._on_menu_add_to_playlist(k, n)
            )
    
    def _on_menu_add_to_playlist(self, key, name):
        track = self.playlist_tree.set(self.menu_iid, "filepath")
        self.playlist_manager.add_to_user_playlist(key, name, Path(track))
        self.menu_iid = None

    def _on_menu_update_favorite(self):
        self._update_favorite(self.menu_iid)
        
    def _update_favorite(self, iid):
        if iid is None or not self.playlist_tree.exists(iid):
            print("playlist_display: _update_favorite, iid is None or doesn't exit")
            return
        
        value = self.playlist_tree.set(iid, column="favorite")
        filepath = self.playlist_tree.set(iid, column="filepath")

        if value == " ☆ ":
            self.playlist_tree.set(iid, column="favorite", value=" ★ ")
            self.favorites[filepath] = True
        elif value == " ★ ":
            self.playlist_tree.set(iid, column="favorite", value=" ☆ ")
            self.favorites[filepath] = False
        self.save_favorites()


    def save_favorites(self):
        path = Path("data/favorites.json")
        try: 
            with path.open("w", encoding="utf-8") as f:
                json.dump(self.favorites, f, indent=2)
        except Exception as e:
            print(f"Failed to save favorites: {e}")

    def load_favorites(self):
        path = Path("data/favorites.json")

        if not path.exists():
            self.favorites = {}
            return
        
        try: 
            with path.open("r", encoding="utf-8") as f:
                self.favorites = json.load(f)
        except Exception as e:
            print(f"Failed to load favorites: {e}")
            self.favorites = {}

    def show_favorites(self):
        self.clear_playlist()
        path = Path("data/favorites.json")

        if not path.exists():
            self.favorites = {}
            return
        
        with path.open("r", encoding="utf-8") as f:
            favorites = json.load(f)
        
        favorites_list = [Path(key) for key, value in favorites.items() if value == True]
        favorites_playlist = Playlist("Favorites", favorites_list)        
        self.set_playlist(favorites_playlist)
        return favorites_playlist

    def get_all_artists(self, track_list):
        artist_set = set()
        for track in track_list:
            media = self.player.instance.media_new(track)
            media.parse()
            artist = media.get_meta(vlc.Meta.Artist)
            if artist:
                artist_set.add(artist)
        return sorted(artist_set)
    
    def get_all_albums(self, track_list):
        album_set = set()
        for track in track_list:
            media = self.player.instance.media_new(track)
            media.parse()
            artist = media.get_meta(vlc.Meta.Album)
            if artist:
                album_set.add(artist)
        return sorted(album_set)
    
    def get_artist_tracks(self, artist_album):
        track_list = []
        for iid in self.playlist_tree.get_children():
            artist = self.playlist_tree.item(iid, 'values')
            if artist_album == artist[6]:
                track_list.append(Path(artist[0]))
        playlist = Playlist(f"{artist_album} - All Tracks", track_list)
        self.set_playlist(playlist)
                
    def get_album_tracks(self, artist_album):
        track_list = []
        for iid in self.playlist_tree.get_children():
            album = self.playlist_tree.item(iid, 'values')
            if artist_album == album[7]:
                track_list.append(Path(album[0]))        
        playlist = Playlist(f"{artist_album} - Album Tracks", track_list)
        self.set_playlist(playlist)
        






