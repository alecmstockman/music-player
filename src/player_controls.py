import tkinter as tk
from tkinter import ttk
from .playlist import Playlist
from .playlist_display import PlaylistDisplay
from .track_display import TrackDisplay
from pathlib import Path
import random


class PlayerControls(ttk.Frame):
    def __init__(self, parent, player, track_display, playlist_display, playlist):
        super().__init__(parent)
        self.player = player
        self.playlist = playlist
        self.track_display = track_display
        self.playlist_display = playlist_display

        self.loop_status = None
        self.shuffle = False
        self.play_order = list(range(len(self.playlist.track_list)))
        self.play_index = 0

        self.current_track_title = tk.StringVar()
        self.track = self.playlist.track_list[self.play_index]
        self.current_track_title.set(self.track.stem)

        self.play_pause_btn = ttk.Button(self, text="▶", command=self.toggle_play, takefocus=0, width=2)
        self.previous_btn = ttk.Button(self, text="⏮", command=self.previous_track, takefocus=0, width=2)
        self.next_btn = ttk.Button(self, text="⏭", command=self.next_track, takefocus=0, width=2)
        self.shuffle_btn = ttk.Button(self, text="🔀", command=self.shuffle_playlist, takefocus=0, width=3)
        self.loop_btn = ttk.Button(self, text="🔁", command=self.toggle_loop, takefocus=0, width=2)

        self.columnconfigure(0, weight=1)

        self.shuffle_btn.grid(row=0, column=1, padx=(40, 0))
        self.previous_btn.grid(row=0, column=2)
        self.play_pause_btn.grid(row=0, column=3)
        self.next_btn.grid(row=0, column=4)
        self.loop_btn.grid(row=0, column=5, padx=(0, 10))

    def update_play_order(self):
        self.play_order = list(range(len(self.playlist.track_list)))

    def get_current_track(self):
        index = self.play_order[self.play_index]
        display_index = self.get_display_index()
        self.track = self.playlist.track_list[index]
        self.current_track_title.set(self.track.stem) 
        if display_index != None:
            self.playlist_display.playlist_tree.selection_set(display_index)
        # self.track_display.update_track_display()
        return self.current_track_title
   
    def toggle_play(self, event=None):
        track = self.playlist.track_list[self.play_order[self.play_index]]
        same_playlist = (self.playlist.name == self.playlist_display.playlist.name)

        if self.player.is_playing():
            self.player.pause() 
            self.play_pause_btn.config(text="▶")
            is_now_playing = False
        else:
            self.player.play()
            self.play_pause_btn.config(text="⏸")
            is_now_playing = True

        if same_playlist:
            if self.track.stem == str(track.stem):
                if is_now_playing:
                    self.playlist_display.play_status_icon_playing(self.play_order[self.play_index])
                else:
                    self.playlist_display.play_status_icon_paused(self.play_order[self.play_index])
            else:
                self.playlist_display.clear_play_status()
        else:
            self._update_display_for_current_track(is_now_playing)

    def _update_display_for_current_track(self, is_now_playing):
        children = self.playlist_display.playlist_tree.get_children()

        for child in children:
            item = self.playlist_display.playlist_tree.item(child)["values"]
            filepath = item[0]
            index = item[1]

            if str(self.track) == filepath:
                if is_now_playing:
                    self.playlist_display.play_status_icon_playing(index)
                else:
                    self.playlist_display.play_status_icon_paused(index)
                return

        self.playlist_display.clear_play_status()

    def get_display_index(self):
        if self.playlist.name == self.playlist_display.playlist.name:
            return self.play_order[self.play_index]
        else:
            children = self.playlist_display.playlist_tree.get_children()
            for child in children:
                item = self.playlist_display.playlist_tree.item(child)["values"]
                filepath = item[0]
                index = item[1]
                self.track = self.playlist.track_list[self.play_index] 
                if str(self.track) == filepath:
                    return index
            return None

    def previous_track(self, event=None):
        self.playlist_display.clear_play_status()

        if 0 < self.play_index:
            if self.loop_status != "track":
                self.play_index -= 1
        elif self.play_index == 0 and self.loop_status == "playlist":
            self.play_index = len(self.playlist.track_list) -1

        self._load_current_track()

    def next_track(self, event=None):
        self.playlist_display.clear_play_status()

        if 0 <= self.play_index < len(self.playlist.track_list) -1:
            if self.loop_status != "track":
                self.play_index += 1
        elif self.play_index == len(self.playlist.track_list) - 1 and self.loop_status == "playlist":
            self.play_index = 0

        self._load_current_track()

    def _load_current_track(self):
        if not self.playlist.track_list:
            return
        if self.play_index >= len(self.play_order):
            self.play_index = self.play_order[-1]
        controls_index = self.play_order[self.play_index]
        display_index = self.get_display_index()
        track = self.playlist.track_list[controls_index]

        if self.player.is_playing():
            self.player.load(track)
            self.player.play()
            if display_index != None:
                self.playlist_display.play_status_icon_playing(display_index)
        else:
            self.player.load(track) 
            if display_index != None:
                self.playlist_display.play_status_icon_paused(display_index)
        
        self.playlist_display.menu_iid = display_index
        self.get_current_track()

    def check_play_status(self):
        if self.playlist.name == self.playlist_display.playlist.name:
            return
        else:
            self._update_display_for_current_track(self.player.is_playing())

    def shuffle_playlist(self):
        if not self.playlist.track_list:
            print("No Tracks in playlist")
            return
        
        if self.loop_status != "track":
            if self.shuffle == False:
                self.shuffle = True
                self.shuffle_btn.config(text="🔀*")

                self.play_order = list(range(len(self.playlist.track_list)))
                random.shuffle(self.play_order)
                self.play_order.remove(self.play_index)
                self.play_order.insert(0, self.play_index)

            else:
                self.shuffle = False
                self.shuffle_btn.config(text="🔀")
                self.play_order = list(range(len(self.playlist.track_list)))

    def toggle_loop(self):
        if not self.playlist.track_list:
            print("No Tracks in playlist")
            return
        
        if self.loop_status == None:
            self.loop_status = "playlist"
            self.loop_btn.config(text="🔁*")
        elif self.loop_status == "playlist":
            self.loop_status = "track"
            self.loop_btn.config(text="🔂")
        elif self.loop_status == "track":
            self.loop_btn.config(text="🔁")
            self.loop_status = None

    def play_selection(self, iid):
        self.update_play_order()
        if iid is None:
            print("player_controls: play_selection, iid is None")
            return
        self.playlist_display.clear_play_status()
        self.play_index = self.play_order.index(iid)
        index = self.play_order[self.play_index]
        track = self.playlist.track_list[index]
        self.player.load(track)
        self.player.play()
        self.get_current_track()
        self.toggle_play()
        
    def play_next_track(self):
        self.playlist_display.clear_play_status()

        if 0 <= self.play_index < len(self.playlist.track_list) -1:
            if self.loop_status != "track":
                self.play_index += 1
        elif self.play_index >= len(self.playlist.track_list):
            self.play_index = len(self.playlst.track_list) - 1
        elif self.play_index == len(self.playlist.track_list) - 1 and self.loop_status == "playlist":
            self.play_index = 0

        controls_index = self.play_order[self.play_index]
        display_index = self.get_display_index()
        track = self.playlist.track_list[controls_index]

        self.player.load(track)
        self.player.play()
        if display_index != None:
            self.playlist_display.play_status_icon_playing(display_index)
        
        self.playlist_display.menu_iid = display_index
        self.get_current_track()




