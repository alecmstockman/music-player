import tkinter as tk
from tkinter import ttk
import time
from .playlist import Playlist
from pathlib import Path
import random

class PlayerControls(ttk.Frame):
    def __init__(self, parent, player, Playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = Playlist
        self.loop_status = None
        self.shuffle = False

        self.play_pause_btn = ttk.Button(self, text="▶", command=self.toggle_play, takefocus=0, width=3)
        self.previous_btn = ttk.Button(self, text="⏮", command=self.previous_track, takefocus=0, width=3)
        self.next_btn = ttk.Button(self, text="⏭", command=self.next_track, takefocus=0, width=3)
        self.shuffle_btn = ttk.Button(self, text="🔀", command=self.shuffle_playlist, takefocus=0, width=3)
        self.loop_btn = ttk.Button(self, text="🔁", command=self.toggle_loop, takefocus=0, width=3)

        self.current_track_title = tk.StringVar()
        self.track = self.playlist.track_list[self.playlist.current_index]
        self.current_track_title.set(self.track.stem)
        self.now_playing_label = ttk.Label(self, textvariable=self.current_track_title)
      
        self.shuffle_btn.pack(side="left",)
        self.previous_btn.pack(side="left")
        self.play_pause_btn.pack(side="left")
        self.next_btn.pack(side="left")
        self.loop_btn.pack(side="left")
        self.now_playing_label.pack(side="left", padx=(300))     

    def toggle_play(self, event=None):
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_btn.config(text="▶")
        else:
            self.player.play()
            self.play_pause_btn.config(text="⏸")
    
    def previous_track(self, event=None):
        print(f"Current Index: {self.playlist.current_index}")
        if self.loop_status == "track":
            if self.player.is_playing():
                self.player.load(self.playlist.track_list[self.playlist.current_index])
                self.player.play()
                return
            else:
                self.player.load(self.playlist.track_list[self.playlist.current_index])
                return 
        elif self.loop_status == "playlist":
            if self.playlist.current_index == 0:
                self.playlist.current_index = len(self.playlist.track_list) -1
            
        if self.playlist.current_index <= 0:
            return
        self.playlist.previous()
        if self.player.is_playing():
            self.player.load(self.playlist.track_list[self.playlist.current_index])
            self.player.play()
            self.play_pause_btn.config(text="⏸")
        else:
            self.player.load(self.playlist.track_list[self.playlist.current_index])
        self.track = self.playlist.track_list[self.playlist.current_index]
        self.current_track_title.set(self.track.stem)

    def next_track(self, event=None):
        if self.loop_status == "track":
            if self.player.is_playing():
                self.player.load(self.playlist.track_list[self.playlist.current_index])
                self.player.play()
                return
            else:
                self.player.load(self.playlist.track_list[self.playlist.current_index])
                return 
        elif self.loop_status == "playlist":
            if self.playlist.current_index < self.playlist.playlist_length - 1:
                self.playlist.current_index += 1
            else:
                self.playlist.current_index = 0
        elif self.loop_status == None:
            if self.playlist.current_index < self.playlist.playlist_length - 1:
                self.playlist.current_index += 1
            else:
                return
        
        print(f"Current Index: {self.playlist.current_index}")
        if self.player.is_playing():
            if self.playlist.current_index < self.playlist.playlist_length:
                self.player.load(self.playlist.track_list[self.playlist.current_index])
                self.player.play()
                self.play_pause_btn.config(text="⏸")
        else:
            if self.playlist.current_index < self.playlist.playlist_length:
                self.player.load(self.playlist.track_list[self.playlist.current_index])
        self.track = self.playlist.track_list[self.playlist.current_index]
        self.current_track_title.set(self.track.stem)

    def shuffle_playlist(self):
        print(f"Shuffle was: {self.shuffle}")
        playlist_copy = self.playlist.track_list.copy()
        random.shuffle(playlist_copy)
        
        if self.loop_status != "track":
            if self.shuffle == False:
                self.shuffle = True
                self.shuffle_btn.config(text="🔀*")
            else:
                self.shuffle = False
                self.shuffle_btn.config(text="🔀")

        print(f"Shuffle is now: {self.shuffle}")
        print("Shuffle playlist not implemented yet")

    def toggle_loop(self):
        if self.loop_status == None:
            self.loop_status = "playlist"
            self.loop_btn.config(text="🔁*")
        elif self.loop_status == "playlist":
            self.loop_status = "track"
            self.loop_btn.config(text="🔂")
        elif self.loop_status == "track":
            self.loop_btn.config(text="🔁")
            self.loop_status = None
        print("Loop functionality not complete!")    
        print(f"Status: {self.loop_status}. Playlist length: {self.playlist.playlist_length}")
