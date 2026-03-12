import tkinter as tk
from tkinter import ttk
from .playlist import Playlist
from .playlist_display import PlaylistDisplay
from pathlib import Path

class TrackDisplay(ttk.Frame):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.player = player
        self.current_track_title = tk.StringVar(value="No Track Playing")
        self.now_playing_label = ttk.Label(self, textvariable=self.current_track_title)
        self.now_playing_label.pack(padx=(5))

        self.time_label = tk.Label(self, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
        self.time_label.pack(pady=5)

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
        print('TRACK DISPLAY: set_progress_on_click')
        proportion = event.x / event.widget.winfo_width()
        length = self.player.get_length()
        print(proportion, length)
        if length <= 0: 
            return
        new_time = int(proportion * length)
        print(f"new time: {new_time}")
        self.player.set_time(new_time)

    def update_current_track(self, track):
        print(f"TRACK DISPLAY; update_current_track, track: {track}")
        self.current_track_title.set(track)

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

        self.time_label.config(text=f"{elapsed_str} / {total_str}")
        percent = (elapsed_ms / total_ms * 100) if total_ms > 0 else 0
        self.progress_var.set(percent)
        self.after(100, self.update_time_and_progress)