import tkinter as tk
from tkinter import ttk
from pathlib import Path
import random


class PlayerControls(ttk.Frame):
    def __init__(self, parent, library, playlist, player, track_display, playlist_display):
        super().__init__(parent)
        self.library = library
        self.player = player
        self.playlist = playlist
        self.track_display = track_display
        self.playlist_display = playlist_display

        self.loop_status = None
        self.shuffle = False
        self.play_order = list(range(len(self.playlist.track_id_list)))
        self.play_index = 0

        self.current_track_title = tk.StringVar()
        self.track = self.playlist.track_id_list[self.play_index]
        self.current_track_title.set(self.track.title)

        self.play_pause_btn = ttk.Button(self, text="▶", command=self.toggle_play, takefocus=0, width=3)
        self.previous_btn = ttk.Button(self, text="⏮", command=self.previous_track, takefocus=0, width=2)
        self.next_btn = ttk.Button(self, text="⏭", command=self.next_track, takefocus=0, width=2)
        self.shuffle_btn = ttk.Button(self, text="🔀", command=self.shuffle_playlist, takefocus=0, width=3)
        self.loop_btn = ttk.Button(self, text="🔁", command=self.toggle_loop, takefocus=0, width=3)

        self.columnconfigure(0, weight=1)

        self.shuffle_btn.grid(row=0, column=1, padx=(40, 0))
        self.previous_btn.grid(row=0, column=2)
        self.play_pause_btn.grid(row=0, column=3)
        self.next_btn.grid(row=0, column=4)
        self.loop_btn.grid(row=0, column=5, padx=(0, 10))
    
    def empty_library_on_initialization(self):
        self.track = None
        self.current_track_title.set("No Tracks In Library")
    
    def update_play_order(self):
        self.play_order = list(range(len(self.playlist.track_id_list)))

    def get_current_track(self):
        print("CONTROLS: get_current_track")
        index = self.play_order[self.play_index]
        display_index = self.get_display_index()
        self.track_id = self.playlist.track_id_list[index]
        track = self.library.tracks[self.track_id]

        self.current_track_title.set(track.title) 
        if display_index != None:
            self.playlist_display.playlist_tree.selection_set(self.track_id)

        self.track_display.update_track_display(self.track_id)
        return self.current_track_title
   
    def toggle_play(self, event=None):
        # print("CONTROLS: toggle_play")
        track_id = self.playlist.track_id_list[self.play_order[self.play_index]]
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
            if is_now_playing:
                self.playlist_display.play_status_icon_playing(track_id)
            else:
                self.playlist_display.play_status_icon_paused(track_id)
        else:
            self._update_display_for_current_track(is_now_playing)

    def _update_display_for_current_track(self, is_now_playing):
        track = self.library.tracks[self.track]
        if self.track in self.playlist_display.playlist.track_id_list:
            if is_now_playing:
                self.playlist_display.play_status_icon_playing(track.track_id)
            else:
                self.playlist_display.play_status_icon_paused(track.track_id)
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
                self.track = self.playlist.track_id_list[self.play_index] 
                if str(self.track) == filepath:
                    return index
            return None

    def previous_track(self, event=None):
        print("CONTROLS: previous track")
        self.playlist_display.clear_play_status()

        if 0 < self.play_index:
            if self.loop_status != "track":
                self.play_index -= 1 
        elif self.play_index == 0 and self.loop_status == "playlist":
            self.play_index = len(self.playlist.track_id_list) -1

        self._load_current_track()

    def next_track(self, event=None):
        print("CONTROLS: next track")
        self.playlist_display.clear_play_status()

        if 0 <= self.play_index < len(self.playlist.track_id_list) -1:
            if self.loop_status != "track":
                self.play_index += 1
        elif self.play_index == len(self.playlist.track_id_list) - 1 and self.loop_status == "playlist":
            self.play_index = 0

        self._load_current_track()

    def _load_current_track(self):
        print("LOAD CURRENT TRACK")
        if not self.playlist.track_id_list:
            return
        if self.play_index >= len(self.play_order):
            self.play_index = self.play_order[-1]
        controls_index = self.play_order[self.play_index]
        display_index = self.get_display_index()
        track_id = self.playlist.track_id_list[controls_index]
        track = self.library.tracks[track_id]

        if self.player.is_playing():
            print("is playing")
            self.player.load(track.filepath)
            self.player.play()
            if display_index != None:
                self.playlist_display.play_status_icon_playing(track_id)
        else:
            print("is not playing")
            self.player.load(track.filepath) 
            if display_index != None:
                self.playlist_display.play_status_icon_paused(track_id)
        
        self.playlist_display.menu_iid = display_index
        self.get_current_track()

    def check_play_status(self):
        print("CONTROLS: check_play_status")
        print(self.playlist.name)
        print(self.playlist_display.playlist.name)
        if self.playlist.name == self.playlist_display.playlist.name:
            return
        else:
            self._update_display_for_current_track(self.player.is_playing())

    def shuffle_playlist(self):
        if not self.playlist.track_id_list:
            print("No Tracks in playlist")
            return
        
        if self.loop_status != "track":
            if self.shuffle == False:
                self.shuffle = True
                self.shuffle_btn.config(text="🔀*")

                self.play_order = list(range(len(self.playlist.track_id_list)))
                random.shuffle(self.play_order)
                self.play_order.remove(self.play_index)
                self.play_order.insert(0, self.play_index)

            else:
                self.shuffle = False
                self.shuffle_btn.config(text="🔀")
                self.play_order = list(range(len(self.playlist.track_id_list)))

    def toggle_loop(self):
        if not self.playlist.track_id_list:
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

    def play_selection(self, track_ids):
        print("CONTROLS: play_selection")
        self.update_play_order()
        if track_ids is None:
            print("player_controls: play_selection, iid is None")
            return
        self.playlist_display.clear_play_status()
        print(track_ids)
        track = self.library.tracks[track_ids]
        print(f"controls: play_selection: {self.playlist_display.playlist_tree.index(track.track_id)}")


        selected_track = self.playlist_display.playlist_tree.item(track_ids)
        values = selected_track["values"]
        self.play_index = self.play_order.index(int(values[2]))
        index = self.play_order[self.play_index]
        print(f"index: {index}")
        track_id = self.playlist.track_id_list[index]
        self.track = self.playlist.track_id_list[self.play_index]
        print(f"track_id_list: {self.playlist.track_id_list}")
        print(f"track_id: {track_id}")
        track = self.library.tracks[track_id]
        self.player.load(Path(track.filepath))
        self.player.play()
        self.toggle_play()
        
    def play_next_track(self):
        print("CONTROLS: play_next_track")
        self.playlist_display.clear_play_status()

        if 0 <= self.play_index < len(self.playlist.track_id_list) -1:
            if self.loop_status != "track":
                self.play_index += 1
        elif self.play_index >= len(self.playlist.track_id_list):
            self.play_index = len(self.playlst.track_id_list) - 1
        elif self.play_index == len(self.playlist.track_id_list) - 1 and self.loop_status == "playlist":
            self.play_index = 0

        controls_index = self.play_order[self.play_index]
        display_index = self.get_display_index()
        track = self.playlist.track_id_list[controls_index]

        self.player.load(track)
        self.player.play()
        if display_index != None:
            self.playlist_display.play_status_icon_playing(display_index)
        
        self.playlist_display.menu_iid = display_index
        self.get_current_track()




