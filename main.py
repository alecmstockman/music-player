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
from src.sidebar import Sidebar

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

paned = ttk.PanedWindow(root, orient="horizontal")
paned.pack(fill="both", expand=True)
sidebar_region = ttk.Frame(paned, width=250, style="Border.TFrame")
sidebar_region.pack(side="left", fill="y")
content_region = ttk.Frame(paned, style="Border.TFrame")
content_region.pack(side="top", fill="both", expand=True)
paned.add(sidebar_region, weight=0)
paned.add(content_region, weight=1)

player = VLCPlayer()

p = Path("Music/")
library_all_tracks = [filename for filename in p.rglob('*') if filename.suffix in AUDIO_FILETYPES]
album_dir = p / "albums"
album_dir_list = [filename for filename in album_dir.iterdir() if filename.is_dir()]

library = Playlist("Main Library", library_all_tracks)

sidebar = Sidebar(sidebar_region, library)
sidebar.pack(fill="both", expand=True)
sidebar.set_sidebar()

controls = PlayerControls(top_row_1, player, library)
controls.pack(side="left")
player.load(library.track_list[controls.current_position])

time_label = tk.Label(top_row_2, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
time_label.pack(pady=5)
 
music_window = PlaylistDisplay(content_region, player, library)
music_window.pack(fill="both", expand=True)
music_window.set_playlist(library)


def update_playing_row():
    real_index = controls.play_order[controls.current_position]
    iid = music_window.find_iid_for_index(real_index)
    if not iid:
        return
    music_window.clear_play_status()
    if player.is_playing():
        music_window.playlist_tree.set(iid, column="play status", value="  🔊")
    elif not player.is_playing():
        music_window.playlist_tree.set(iid, column="play status", value="  🔈")
    music_window.playlist_tree.selection_set(iid)
    music_window.playlist_tree.see(iid)

def play_pause_current(event=None):
    controls.toggle_play()
    root.after(100, update_playing_row)

def play_previous(event=None):
    controls.previous_track()
    root.after(100, update_playing_row)

def play_next(event=None):
    controls.next_track()
    root.after(100, update_playing_row)

def play_selected_tracks(event):
    track_values = music_window.get_selected_tracks()
    index = track_values["index"]
    controls.set_index(index)
    track = library.track_list[index]
    
    player.load(track)
    controls.current_track_title.set(track.stem)
    player.play()
    root.after(100, update_playing_row)
    controls.toggle_play()

def quit_app(event=None):
    player.stop()
    root.destroy()

music_window.playlist_tree.bind('<Double-Button-1>', play_selected_tracks)
root.bind("<space>", play_pause_current, add="+")
root.bind("<Left>", play_previous, add="+")
root.bind("<Right>", play_next, add="+")
root.bind("<Command-q>", quit_app, add="+")

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


def schedule_ui_update(controls):
    if hasattr(controls, "_update_job") and controls._update_job:
        root.after_cancel(controls._update_job)
    def delayed_update():
        controls._update_job = None
        update_playing_row()
    controls._update_job = root.after(100, delayed_update)

controls.on_track_changed = schedule_ui_update

player.on_track_finished = lambda autoplay=True: root.after(
    0,
    controls._handle_track_finished,
    autoplay,
)

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