import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.playlist import Playlist
from src.vlc_player import VLCPlayer
# from src.styles import setup_styles
from src.config import AUDIO_FILETYPES


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, player, playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = playlist

        self.playlist_tree = ttk.Treeview(
            self, 
            columns=("filepath", "index", "play status", "Track", "Time", "Artist", "Album", "favorite", "Filetype", "Blank"), 
            show="headings"
        )
        self.playlist_tree.pack(side="left", fill="both", expand=True)
        
        self.playlist_tree.column("filepath", width=0, stretch=False)
        self.playlist_tree.column("index", width=0, stretch=False)
        self.playlist_tree.column("play status", anchor="w", width=40, stretch=False)
        self.playlist_tree.column("Track", anchor="w", width=400, stretch=False)
        self.playlist_tree.column("Time", anchor="e", width=80, stretch=False)
        self.playlist_tree.column("Artist", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Album", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Filetype", anchor="e", width=100, stretch=False)
        self.playlist_tree.column("favorite", anchor="e", width=40, stretch=False)
        self.playlist_tree.column("Blank", anchor="w", width=200, stretch=True)
        
        self.playlist_tree.heading("filepath")
        self.playlist_tree.heading("index")
        self.playlist_tree.heading("play status", text="  ")
        self.playlist_tree.heading("Track", text="Title")
        self.playlist_tree.heading("Time", text="Length")
        self.playlist_tree.heading("Artist", text="Artist")
        self.playlist_tree.heading("Album", text="Album")
        self.playlist_tree.heading("favorite", text="  ")
        self.playlist_tree.heading("Filetype", text="Filetype")
        self.playlist_tree.heading("Blank", text="")


    def set_playlist(self, playlist):
        print("SET PLAYLIST")
        index = 0
        even = True

        for track in self.playlist.track_list:
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
                        values=(filepath, f"{track_index}", "", f"{title}", f"{total_str}", f"{artist}", f"{album}", " ☆ ", f"{filetype}"),
                        tags="even" 
                    )
                    even = False
                else:
                    self.playlist_tree.insert(
                        "", "end",
                        iid=str(track_index), 
                        values=(filepath, f"{track_index}", "", f"{title}", f"{total_str}", f"{artist}", f"{album}", " ☆ ", f"{filetype}"),
                        tags="odd" 
                    )
                    even = True
                index += 1

    def get_selected_tracks(self):
        selection = self.playlist_tree.selection()
        print(f"Get selected tracks, selection: {selection}")
        if not selection:
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
    
    
    def update_play_status_column(self):
        self.playlist_display.playlist_tree.set(iid, column="play status", value="  🔊")
        self.playlist_display.playlist_tree.set(iid, column="play status", value="  🔈")
        pass
