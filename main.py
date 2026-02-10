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
from src.music_window import PlaylistDisplay

root = tk.Tk()
root.lift()
root.focus_force()
root.title("No Vibe Music Player")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

setup_styles(root)

top_region = ttk.Frame(root, style="Border.TFrame")
top_region.pack(side="top", fill="x")
top_row_1 = ttk.Frame(top_region)
top_row_1.pack(side="top", fill="x")
top_row_2 = ttk.Frame(top_region)
top_row_2.pack(side="top", fill="x")
sidebar_region = ttk.Frame(root, width=300, style="Border.TFrame")
sidebar_region.pack(side="left", fill="y")
content_region = ttk.Frame(root, style="Border.TFrame")
content_region.pack(side="top", fill="both", expand=True)

player = VLCPlayer()

p = Path("Music/")
library_all_tracks = [filename for filename in p.rglob('*') if filename.suffix in AUDIO_FILETYPES]
album_dir = p / "albums"
album_dir_list = [filename for filename in album_dir.iterdir() if filename.is_dir()]

library = Playlist("Main Library", library_all_tracks)

controls = PlayerControls(top_row_1, player, library)
controls.pack(side="left")
print(library.track_list[library.current_index])
player.load(library.track_list[library.current_index])

time_label = tk.Label(top_row_2, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
time_label.pack(pady=5)

music_window = PlaylistDisplay(content_region, player, library)
music_window.pack(fill="both", expand=True)
music_window.set_playlist()

# def play_selected_track(self):
#     pass

music_window.bind('<Double-Button-1>', music_window.play_selected_track)

def quit_app(event=None):
    player.stop()
    root.destroy()

root.bind("<space>", controls.toggle_play, add="+")
root.bind("<Left>", controls.previous_track, add="+")
root.bind("<Right>", controls.next_track, add="+")
root.bind("<Command-q>", quit_app, add="+")

def play_next():
    library.next()
    if library.current_index >= len(library.track_list) - 1:
        return
    else:
        track = library.track_list[library.current_index]
        player.load(library.track_list[library.current_index])
        controls.current_track_title.set(track.stem)
        player.play()

player.on_track_finished = lambda: root.after(0, play_next)

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
        command=set_audio_volume
    )
volume_slider.set(80)
volume_slider.pack(padx=150, pady=10)

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
    set_progress_on_click
    progress_var.set(percent)

    root.after(25, update_time_and_progress)


def test_prints():
    print("\n--- SONGS IN PLAYLIST ---")
    count = 1
    for song in library_all_tracks:
        print(f"{count}: {song}")
        count += 1
    print("\n")

test_prints()
update_time_and_progress()
root.mainloop()