import tkinter as tk
from tkinter import ttk
import time
from .playlist import Playlist
from .music_window import PlaylistDisplay
from pathlib import Path
import random

class PlayerControls(ttk.Frame):
    def __init__(self, parent, player, playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = playlist

        self.play_order = list(range(len(self.playlist.track_list)))
        self.current_position = 0

        self.loop_status = None
        self.shuffle = False
        self.player.on_track_end = self._handle_track_finished
        self.player.on_track_finished = self._handle_track_finished
        self.on_track_changed = None
        self._update_job = None

        self.play_pause_btn = ttk.Button(self, text="▶", command=self.toggle_play, takefocus=0, width=3)
        self.previous_btn = ttk.Button(self, text="⏮", command=self.previous_track, takefocus=0, width=3)
        self.next_btn = ttk.Button(self, text="⏭", command=self.next_track, takefocus=0, width=3)
        self.shuffle_btn = ttk.Button(self, text="🔀", command=self.shuffle_playlist, takefocus=0, width=3)
        self.loop_btn = ttk.Button(self, text="🔁", command=self.toggle_loop, takefocus=0, width=3)

        self.current_track_title = tk.StringVar()
        self.track = self.playlist.track_list[self.current_position]
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
        if self.loop_status == "track":
            real_index = self.play_order[self.current_position]
            track = self.playlist.track_list[real_index]
            if self.player.is_playing():
                self.player.load(track)
                self.player.play()
            else:
                self.player.load(track)
            return
        
        if self.current_position > 0:
            self.current_position -= 1
        else:
            if self.loop_status == "playlist":
                self.current_position = len(self.play_order) - 1
            else:
                return
        real_index = self.play_order[self.current_position]
        track = self.playlist.track_list[real_index]
        self.current_track_title.set(track.stem)
        if self.player.is_playing():
            self.player.load(track)
            self.player.play()
        else:
            self.player.load(track)

    def next_track(self, event=None, autoplay=False):
        was_playing = self.player.is_playing()
        # print(f"START - was_playing: {was_playing}, autoplay: {autoplay}")

        if self.loop_status == "track":
            real_index = self.play_order[self.current_position]
            track = self.playlist.track_list[real_index]
            self.player.load(track)
            if was_playing or autoplay:
                self.player.play()
            if self.on_track_changed:
                self._fire_track_changed()
                # self.on_track_changed()
            return

        if self.current_position < len(self.play_order) - 1:
            self.current_position += 1
        else:
            if self.loop_status == "playlist":
                self.current_position = 0
            else:
                return
            
        real_index = self.play_order[self.current_position]
        track = self.playlist.track_list[real_index]
        self.current_track_title.set(track.stem)
        self.player.load(track)

        if was_playing or autoplay:
            self.player.play()
        if self.on_track_changed:
            self._fire_track_changed()
            # self.on_track_changed()


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
        print(f"Shuffle is now: {self.shuffle}")

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

    def set_index(self, index: int):
        if 0 <= index < len(self.play_order):
            self.current_position = index
        return self.current_position

    def _handle_track_finished(self, autoplay=True):
        self.next_track(autoplay=autoplay)

    def _fire_track_changed(self):
        if self.on_track_changed:
            self.on_track_changed(self)