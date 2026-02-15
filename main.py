import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from src.player_controls import PlayerControls
from src.vlc_player import VLCPlayer
from src.playlist import Playlist
# from src.styles import setup_styles
from src.config import AUDIO_FILETYPES
from src.playlist_display import PlaylistDisplay
from src.sidebar import Sidebar
import random

root = tk.Tk()
root.lift()
root.focus_force()
root.title("No Vibe Music Player - VERSION 2")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

top_region = ttk.Frame(root, style="Border.TFrame")
top_region.pack(side="top", fill="x")
top_row_1 = ttk.Frame(top_region)
top_row_1.pack(side="top", fill="x")
top_row_2 = ttk.Frame(top_region)
top_row_2.pack(side="top", fill="x")

paned = ttk.PanedWindow(root, orient="horizontal")
paned.pack(fill="both", expand=True)
sidebar_region = ttk.Frame(paned, width=250, style="Border.TFrame")
sidebar_region.pack(side="left", fill="y")
content_region = ttk.Frame(paned, style="Border.TFrame")
content_region.pack(side="top", fill="both", expand=True)
paned.add(sidebar_region, weight=0)
paned.add(content_region, weight=1)

player = VLCPlayer()
event_manager = player.player.event_manager()
event_manager.event_attach(
    vlc.EventType.MediaPlayerEndReached,
    lambda event: root.after(50, controls.play_next_track)
)

p = Path("Music/")
library_all_tracks = [filename for filename in p.rglob('*') if filename.suffix in AUDIO_FILETYPES]
album_dir = p / "albums"
album_dir_list = [filename for filename in album_dir.iterdir() if filename.is_dir()]

library = Playlist("Main Library", library_all_tracks)

playlist_display = PlaylistDisplay(content_region, player, library)
playlist_display.pack(fill="both", expand=True)
playlist_display.set_playlist(library)

controls = PlayerControls(top_row_1, player, playlist_display, library)
controls.pack(side="left")
playlist_display.controls = controls
player.load(library.track_list[controls.play_index])
time_label = tk.Label(top_row_2, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
time_label.pack(pady=5)

player.load(library.track_list[controls.play_index])


sidebar = Sidebar(sidebar_region, library)
sidebar.pack(fill="both", expand=True)
sidebar.set_sidebar()

root.bind("<space>", controls.toggle_play, add="+")
root.bind("<Left>", controls.previous_track, add="+")
root.bind("<Right>", controls.next_track, add="+")



def play_selected_tracks(event):
    track_values = playlist_display.get_selected_tracks()
    iid = track_values["index"]
    controls.play_selection(iid)

playlist_display.playlist_tree.bind('<Double-Button-1>', play_selected_tracks)


progress_var = tk.DoubleVar()
def set_progress_on_click(event):
    proportion = event.x / event.widget.winfo_width()
    length = player.get_length()
    if length <= 0:
        return
    new_time = int(proportion * length)
    player.set_time(new_time)

progress_bar = ttk.Progressbar(
    top_row_2,
    orient="horizontal", 
    length=500, 
    maximum=100, 
    mode="determinate", 
    variable=progress_var
    )

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
    progress_var.set(percent)
    root.after(100, update_time_and_progress)

progress_bar.pack(pady=5)
progress_bar.bind('<Button-1>', set_progress_on_click, add="+")
progress_bar.bind('<B1-Motion>', set_progress_on_click, add="+")


def set_audio_volume(val):
    volume_level = int(float(val))
    player.set_volume(volume_level)

volume_slider = ttk.Scale(
        top_row_1,
        orient="horizontal",
        from_=0,
        to=100,
        command=set_audio_volume,
        length = 120
    )
volume_slider.set(80)
volume_slider.pack(padx=100, pady=10)

def quit_app(event=None):
    player.stop()
    root.destroy()
root.bind("<Command-q>", quit_app, add="+")



def test_function():
    print("\n--- SONGS IN PLAYLIST ---")
    count = 1
    for song in library_all_tracks:
        print(f"{count}: {song}")
        count += 1
    print("\n")
    
test_function()
update_time_and_progress()
root.mainloop()