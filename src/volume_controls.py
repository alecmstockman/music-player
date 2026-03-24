import tkinter as tk
from tkinter import ttk
from pathlib import Path
import random

class VolumeControls(ttk.Frame):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.player = player

        self.volume_slider = ttk.Scale(
                parent,
                orient="horizontal",
                from_=0,
                to=100,
                command=self.set_audio_volume,
                length = 100
            )

        self.volume_slider.set(80)
        self.volume_slider.pack(padx=100, pady=10)
 
        
    def set_audio_volume(self, val):
        volume_level = int(float(val))
        self.player.set_volume(volume_level)

    def volume_up(self, event):
        volume  = self.player.player.audio_get_volume()
        if volume <= 95:
            self.set_audio_volume(volume + 5)
            self.volume_slider.set(volume + 5)
            return "break"
        else:
            self.set_audio_volume(100)
            self.volume_slider.set(100)
            return "break"

    def volume_down(self, event):
        volume = self.player.player.audio_get_volume()
        if volume >= 5:
            self.set_audio_volume(volume - 5)
            self.volume_slider.set(volume -5)
            return "break"
        else:
            self.set_audio_volume(0)
            self.volume_slider.set(0)
            return "break"

        
        