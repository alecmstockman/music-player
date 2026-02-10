import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.playlist import Playlist
from src.vlc_player import VLCPlayer
from src.styles import setup_styles
from src.config import AUDIO_FILETYPES


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, player, Playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = Playlist

        self.playlist_tree = ttk.Treeview(self, columns=("filepath", "Play Status", "Track", "Time", "Artist", "Album", "Filetype", "Blank"), show="headings")
        self.playlist_tree.pack(side="left", fill="both", expand=True)
        self.playlist_tree.bind('<Double-Button-1>', self.play_selected_track)
        
        self.playlist_tree.column("filepath", width=0, stretch=False)
        self.playlist_tree.column("Play Status", anchor="w", width=50, stretch=False)
        self.playlist_tree.column("Track", anchor="w", width=400, stretch=False)
        self.playlist_tree.column("Time", anchor="e", width=80, stretch=False)
        self.playlist_tree.column("Artist", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Album", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Filetype", anchor="e", width=100, stretch=False)
        self.playlist_tree.column("Blank", anchor="w", width=200, stretch=True)
        
        self.playlist_tree.heading("filepath")
        self.playlist_tree.heading("Play Status", text="  ")
        self.playlist_tree.heading("Track", text="Title")
        self.playlist_tree.heading("Time", text="Length")
        self.playlist_tree.heading("Artist", text="Artist")
        self.playlist_tree.heading("Album", text="Album")
        self.playlist_tree.heading("Filetype", text="Filetype")
        self.playlist_tree.heading("Blank", text="")
        
    def set_playlist(self):
        index = 0
        for track in self.playlist.track_list:
            media = self.player.instance.media_new(track)
            media.parse()

            filepath = self.playlist.track_list[index]
            index += 1
            title = media.get_meta(vlc.Meta.Title)
            artist = media.get_meta(vlc.Meta.Artist)
            album = media.get_meta(vlc.Meta.Album)
            total_s = media.get_duration() // 1000
            total_str = f"{total_s//60:d}:{total_s%60:02d}"
            filetype = track.suffix[1:]

            if track.suffix in AUDIO_FILETYPES:
                self.playlist_tree.insert(
                    "", "end", 
                    values=(filepath, "", f"{title}", f"{total_str}", f"{artist}", f"{album}", f"{filetype}"), 
                )
    


    def play_selected_track(self, event):
        track = event.widget
        selected_tracks = track.selection()
        for item_iid in selected_tracks:
            item = track.item(item_iid)
            filepath = item["values"][0]
            self.player.load(filepath)
            self.player.play
            print(filepath)
            # print(track.item(item_iid))
            # item = track.item(item_iid)

        # self.player.load(track)

