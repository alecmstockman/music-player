import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from .playlist import Playlist
from vlc_player import VLCPlayer
from styles import setup_styles


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, Playlist):
        super.__init__(parent)
        
