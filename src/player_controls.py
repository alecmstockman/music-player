import tkinter as tk
from tkinter import ttk
import time
from .playlist import Playlist
from .playlist_display import PlaylistDisplay
from pathlib import Path
import random

class PlayerControls(ttk.Frame):
    def __init__(self, parent, player, playlist_display, playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = playlist
        self.playlist_display = playlist_display

        self.loop_status = None
        self.shuffle = False
        self.play_order = list(range(len(self.playlist.track_list)))
        self.play_index = 0

        self.current_track_title = tk.StringVar()
        self.track = self.playlist.track_list[self.play_index]
        self.current_track_title.set(self.track.stem)
        self.now_playing_label = ttk.Label(self, textvariable=self.current_track_title)

        self.play_pause_btn = ttk.Button(self, text="▶", command=self.toggle_play, takefocus=0, width=3)
        self.previous_btn = ttk.Button(self, text="⏮", command=self.previous_track, takefocus=0, width=3)
        self.next_btn = ttk.Button(self, text="⏭", command=self.next_track, takefocus=0, width=3)
        self.shuffle_btn = ttk.Button(self, text="🔀", command=self.shuffle_playlist, takefocus=0, width=3)
        self.loop_btn = ttk.Button(self, text="🔁", command=self.toggle_loop, takefocus=0, width=3)

        self.shuffle_btn.pack(side="left",)
        self.previous_btn.pack(side="left")
        self.play_pause_btn.pack(side="left")
        self.next_btn.pack(side="left")
        self.loop_btn.pack(side="left")
        self.now_playing_label.pack(side="left", padx=(300))   

    def get_current_track(self):
        # print(f"play order: {self.play_order}, play index; {self.play_index}")
        index = self.play_order[self.play_index]
        self.track = self.playlist.track_list[index]
        self.current_track_title.set(self.track.stem)

    def toggle_play(self, event=None):
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_btn.config(text="▶")
            self.playlist_display.play_status_icon_paused(self.play_order[self.play_index])
            # print("toggle_play: PAUSED")
        else:
            self.player.play()
            self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
            self.play_pause_btn.config(text="⏸")
            # print("toggle_play: PLAYING")

    def previous_track(self, event=None):
        self.playlist_display.clear_play_status()
        if self.loop_status == "track":
            index = self.play_order[self.play_index]
            track = self.playlist.track_list[index]
            if self.player.is_playing():
                self.player.load(track)
                self.player.play()
                self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
            else:
                self.player.load(track)
                self.playlist_display.play_status_icon_paused(self.play_order[self.play_index])
            return
        
        if self.play_index > 0:
            self.play_index -= 1
        else:
            if self.loop_status == "playlist":
                self.play_index = len(self.playlist.track_list) -1
            else:
                self.play_index = 0
        index = self.play_order[self.play_index]
        track = self.playlist.track_list[index]
        if self.player.is_playing():
            self.player.load(track)
            self.player.play()
            self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
        else:
            self.player.load(track)
            self.playlist_display.play_status_icon_paused(self.play_order[self.play_index])
        self.get_current_track()

        print(f"Previous_track, play index now {self.play_index}")


    def next_track(self, event=None):
        self.playlist_display.clear_play_status()
        if self.loop_status == "track":
            index = self.play_order[self.play_index]
            track = self.playlist.track_list[index]
            if self.player.is_playing():
                self.player.load(track)
                self.player.play()
                self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
            else:
                self.player.load(track)
                self.playlist_display.play_status_icon_paused(self.play_order[self.play_index])
            return

        if 0 <= self.play_index < len(self.playlist.track_list) -1:
            self.play_index += 1
        else:
            if self.loop_status == "playlist":
                self.play_index = 0
            else:
                self.play_index = len(self.playlist.track_list) - 1
        index = self.play_order[self.play_index]
        track = self.playlist.track_list[index]
        if self.player.is_playing():
            self.player.load(track)
            self.player.play()
            self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
        else:
            self.player.load(track)
            self.playlist_display.play_status_icon_paused(self.play_order[self.play_index])
        self.get_current_track()
        print(f"Next_track, play index now {self.play_index}")


    def shuffle_playlist(self):
        if self.loop_status != "track":
            if self.shuffle == False:
                self.shuffle = True
                self.shuffle_btn.config(text="🔀*")
                self.play_order = list(range(len(self.playlist.track_list)))
                random.shuffle(self.play_order)
            else:
                self.shuffle = False
                self.shuffle_btn.config(text="🔀")
                self.play_order = list(range(len(self.playlist.track_list)))
        print(f"Shuffle is now: {self.shuffle}, DOES NOT FUNCTION YET!")


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
        print(f"Loop is now: {self.loop_status}")

    def play_selection(self, iid):
        self.playlist_display.clear_play_status()
        self.play_index = self.play_order.index(iid)
        index = self.play_order[self.play_index]
        track = self.playlist.track_list[index]
        print(f"IID: {iid}")
        print("PLAY SELECTION")
        print(f"Play index: {self.play_index}, index: {index}, track: {track} \n")
        self.player.load(track)
        self.player.play()
        self.get_current_track()
        self.toggle_play()
        

    def play_next_track(self):
        if self.loop_status == "track":
            index = self.play_order[self.play_index]
            track = self.playlist.track_list[index]
            self.player.load(track)
            self.player.play()
            self.get_current_track()
            return
        
        if 0 <= self.play_index < len(self.playlist.track_list) -1:
            self.play_index += 1
        else:
            if self.loop_status == "playlist":
                self.play_index = 0
            else:
                self.play_index = len(self.playlist.track_list) - 1
                self.toggle_play()
                return
        index = self.play_order[self.play_index]
        track = self.playlist.track_list[index]
        self.player.load(track)
        self.player.play()
        self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
        self.get_current_track()


