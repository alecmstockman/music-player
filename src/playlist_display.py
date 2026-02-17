import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.playlist import Playlist
from src.vlc_player import VLCPlayer
# from .player_controls import PlayerControls
# from src.styles import setup_styles
from src.config import AUDIO_FILETYPES


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, player, playlist, ):
        super().__init__(parent)
        self.player = player
        self.playlist = playlist
        
        self.popup_menu = tk.Menu(self, tearoff=False)
        self.playlist_submenu = tk.Menu(self.popup_menu, tearoff=False)
        self.menu_iid = None

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
        # self.popup_menu.add_command(label="Add to Playlist", command=self._on_menu_test)
        self.popup_menu.add_cascade(label="Add to Playlist", menu=self.playlist_submenu)
        self.playlist_submenu.add_command(label="Playlist One", state="disabled")
        self.playlist_submenu.add_command(label="Playlist Two", state="disabled")
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Favorite", command=self._on_menu_update_favorite)
        self.popup_menu.add_command(label="Remove Favorite", command=self._on_menu_update_favorite)


    def set_playlist(self, playlist):
        if not playlist or not hasattr(playlist, "track_list"):
            print("No playlist or invalid playlist object")
            return
        print("SET PLAYLIST")
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

            if track.suffix in AUDIO_FILETYPES:
                track_index = index
                if even is True:
                    self.playlist_tree.insert(
                        "", "end",
                        iid=str(track_index),
                        values=(filepath, f"{track_index}", "", f"{title}", "···", f"{total_str}", f"{artist}", f"{album}", " ☆ ", f"{filetype}"),
                        tags="even" 
                    )
                    even = False
                else:
                    self.playlist_tree.insert(
                        "", "end",
                        iid=str(track_index), 
                        values=(filepath, f"{track_index}", "", f"{title}", "···", f"{total_str}", f"{artist}", f"{album}", " ☆ ", f"{filetype}"),
                        tags="odd" 
                    )
                    even = True
                index += 1

    def get_selected_tracks(self):
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
            self.playlist_tree.set(iid, column="play status", value="")

    def remove_play_status_icon(self, index):
        if index is None:
            print("playlist_display: remove_play_status_icon, index is None")
            return
        iid = index
        self.playlist_tree.set(iid, column="play status", value="   ")

    def play_status_icon_playing(self, index):
        if index is None:
            print("playlist_display: play_status_icon_playing, index is None")
            return
        iid = index
        self.playlist_tree.set(iid, column="play status", value="  🔊")

    def play_status_icon_paused(self, index):
        if index is None:
            print("playlist_display: play_status_icon_paused, index is None")
            return
        iid = index
        self.playlist_tree.set(iid, column="play status", value="  🔈")

    def on_tree_click(self, event):
        row_id = self.playlist_tree.identify_row(event.y)
        col_id = self.playlist_tree.identify_column(event.x)
        self.menu_iid = row_id
        print(f"Row ID: {row_id}, Col ID: {col_id}")
        if col_id == "#5":
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        if col_id == "#9":
            self._update_favorite(self.menu_iid)

    def _on_menu_test(self):
        # print("menu clicked")
        pass

    def _on_menu_play(self):
        print(f"MENU IID; {self.menu_iid}")
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

    def _on_menu_add_to_playlist(self):
        pass

    def _on_menu_update_favorite(self):
        self._update_favorite(self.menu_iid)
        
    def _update_favorite(self, iid):
        if iid is None or not self.playlist_tree.exists(iid):
            print("playlist_display: _update_favorite, iid is None or doesn't exit")
            return
        
        value = self.playlist_tree.set(iid, column="favorite")

        if value == " ☆ ":
            self.playlist_tree.set(iid, column="favorite", value=" ★ ")
        elif value == " ★ ":
            self.playlist_tree.set(iid, column="favorite", value=" ☆ ")





