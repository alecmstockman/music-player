import tkinter as tk
from tkinter import ttk
import time

class PlayerControls(ttk.Frame):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.player = player

        self.play_pause_btn = ttk.Button(self, text="▶", command=self.toggle_play)
        self.previous_btn = ttk.Button(self, text="⏮", command=self.previous_track)
        self.next_btn = ttk.Button(self, text="⏭", command=self.next_track)

        self.previous_btn.pack(side="left")
        self.play_pause_btn.pack(side="left")
        self.next_btn.pack(side="left")

    def toggle_play(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_btn.config(text="▶")
        else:
            self.player.play()
            self.play_pause_btn.config(text="⏸")
    
    def previous_track(self):
        print("Previous track (not implemented yet)")

    def next_track(self):
        print("Next track (not implemented yet)")