from tkinter import ttk
from pathlib import Path
from .config import AUDIO_FILETYPES

def songs_view():
    # album_list = os.listdir("Music/Albums/")
    print(AUDIO_FILETYPES)
    p = Path("Music/")
    song_list = [filename for filename in p.rglob('*') if filename.suffix in AUDIO_FILETYPES]

    for song in song_list:
        print(song)
