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

root = tk.Tk()
root.lift()
root.focus_force()
root.title("No Vibe Music Player")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

setup_styles(root)

top_region = ttk.Frame(root)
top_region.pack(side="top", fill="x")
content_region = ttk.Frame(root)
content_region.pack(side="top", fill="both", expand=True)

player = VLCPlayer()

p = Path("Music/")
library_all_tracks = [filename for filename in p.rglob('*') if filename.suffix in AUDIO_FILETYPES]
album_dir = p / "albums"
album_dir_list = [filename for filename in album_dir.iterdir() if filename.is_dir()]

library = Playlist("Main Library", library_all_tracks)

# ACTIVE_PLAYLIST = library
controls = PlayerControls(top_region, player, library)
controls.pack(side="left")
print(library.track_list[library.current_index])
player.load(library.track_list[library.current_index])


time_label = tk.Label(content_region, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
time_label.pack(pady=5)
progress_bar = ttk.Progressbar(content_region, orient="horizontal", length=480, mode="determinate")
progress_bar.pack(pady=4)

def update_time_and_progress():
    elapsed_ms = player.player.get_time()
    total_ms = player.player.get_length()

    if elapsed_ms == -1:
        elapsed_ms = 0
    if total_ms <= 0:
        total_ms = 0

    elapsed_s = elapsed_ms // 1000
    total_s = total_ms // 1000
    elapsed_str = f"{elapsed_s//60:02d}:{elapsed_s%60:02d}"
    total_str = f"{total_s//60:02d}:{total_s%60:02d}"

    time_label.config(text=f"{elapsed_str} / {total_str}")
    percent = (elapsed_ms / total_ms * 100) if total_ms > 0 else 0
    progress_bar['value'] = percent

    root.after(25, update_time_and_progress)

def test_prints():

    print("\n--- SONGS IN PLAYLIST ---")
    for song in library_all_tracks:
        print(song)
    print("\n")

test_prints()
update_time_and_progress()
root.mainloop()