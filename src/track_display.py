import tkinter as tk
from tkinter import ttk
from .playlist import Playlist
from .playlist_display import PlaylistDisplay
from pathlib import Path

class TrackDisplay(ttk.Frame):
    def __init__(self, parent, library, player):
        super().__init__(parent)
        self.library = library
        self.player = player
        self.current_track_title = tk.StringVar(value="No Track Playing")
        self.current_artist_and_album = tk.StringVar(value="No Album Playing")

        self.now_playing_track_label = ttk.Label(self, textvariable=self.current_track_title)
        self.now_playing_track_label.pack(padx=(5), pady=5)

        self.now_playing_album_label = ttk.Label(self, textvariable=self.current_artist_and_album)
        self.now_playing_album_label.pack(padx=(5))

        self.time_elapsed_label = tk.Label(self, text="00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
        self.total_time_label = tk.Label(self, text="00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
        self.time_elapsed_label.pack(side="left", padx=(150, 0))
        self.total_time_label.pack(side="right", padx=(0, 150))

        self.progress_var = tk.DoubleVar()

        self.progress_bar = ttk.Progressbar(
        self,
        orient="horizontal", 
        length=300, 
        maximum=100, 
        mode="determinate", 
        variable=self.progress_var
        )

        self.progress_bar.pack(pady=5)
        self.progress_bar.bind('<Button-1>', self.set_progress_on_click, add="+")
        self.progress_bar.bind('<B1-Motion>', self.set_progress_on_click, add="+")

    def set_progress_on_click(self, event):
        proportion = event.x / event.widget.winfo_width()
        length = self.player.get_length()
        if length <= 0: 
            return
        new_time = int(proportion * length)
        self.player.set_time(new_time)

    def update_track_display(self, track_id):
        track = self.library.tracks[track_id]
        self.current_track_title.set(track.title)
        self.current_artist_and_album.set(f"{track.artist}: {track.album}") 

    def update_time_and_progress(self):
        elapsed_ms = self.player.player.get_time()
        total_ms = self.player.player.get_length()

        if elapsed_ms == -1:
            elapsed_ms = 0
        if total_ms <= 0:
            total_ms = 0

        elapsed_s = elapsed_ms // 1000
        total_s = total_ms // 1000
        elapsed_str = f"{elapsed_s//60:02d}:{elapsed_s%60:02d}"
        total_str = f"{total_s//60:02d}:{total_s%60:02d}"

        self.time_elapsed_label.config(text=f"{elapsed_str}")
        self.total_time_label.config(text=f"{total_str}")
        percent = (elapsed_ms / total_ms * 100) if total_ms > 0 else 0
        self.progress_var.set(percent)
        self.after(100, self.update_time_and_progress)