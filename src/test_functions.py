import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.top_banner import PlayerControls
from src.vlc_player import VLCPlayer
from src.styles import setup_styles
from src.playlist import Playlist
from src.config import AUDIO_FILETYPES


config = {
'command': ('command', 'command', 'Command', '', <bytecode object: '4360071104toggle_loop'>), 
 'default': ('default', 'default', 'Default', <index object: 'normal'>, <index object: 'normal'>), 
 'takefocus': ('takefocus', 'takeFocus', 'TakeFocus', 'ttk::takefocus', 'ttk::takefocus'), 
 'text': ('text', 'text', 'Text', '', '🔁'), 
 'textvariable': ('textvariable', 'textVariable', 'Variable', '', ''), 
 'underline': ('underline', 'underline', 'Underline', -1, -1), 
 'width': ('width', 'width', 'Width', '', ''), 
 'image': ('image', 'image', 'Image', '', ''), 
 'compound': ('compound', 'compound', 'Compound', '', ''), 
 'padding': ('padding', 'padding', 'Pad', '', ''), 
 'state': ('state', 'state', 'State', <index object: 'normal'>, <index object: 'normal'>), 
 'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 
 'style': ('style', 'style', 'Style', '', ''), 
 'class': ('class', '', '', '', '')
 }
