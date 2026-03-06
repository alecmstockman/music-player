import tkinter as tk
from tkinter import ttk
import vlc
from pathlib import Path
from src.player_controls import PlayerControls
from src.vlc_player import VLCPlayer
from src.playlist import Playlist, PlaylistManager
from src.styles import setup_styles
from src.config import AUDIO_FILETYPES
from src.playlist_display import PlaylistDisplay
from src.sidebar import Sidebar, SecondarySidebar
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
sidebar_region = ttk.Frame(paned, width=200, style="Border.TFrame")
sidebar_region.pack(side="left", fill="y")
paned.add(sidebar_region, weight=0)

secondary_sidebar_region = ttk.Frame(paned, width=300, style="Border.TFrame")

playlist_display_region = ttk.Frame(paned, style="Border.TFrame")
playlist_display_region.pack(side="top", fill="both", expand=True)
paned.add(playlist_display_region, weight=1)

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
playlist_manager = PlaylistManager(library)

playlist_display = PlaylistDisplay(playlist_display_region, player, library, playlist_manager)
playlist_display.pack(fill="both", expand=True)
playlist_display.set_playlist(library)

controls = PlayerControls(top_row_1, player, playlist_display, library)
controls.pack(side="left")
playlist_display.controls = controls
player.load(library.track_list[controls.play_index])
time_label = tk.Label(top_row_2, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="CadetBlue")
time_label.pack(pady=5)

player.load(library.track_list[controls.play_index])
playlist_manager.load_playlist()
playlist_display._set_popup_playlist_list()

sidebar = Sidebar(sidebar_region, library, playlist_manager)
sidebar.pack(fill="both", expand=True)
sidebar.set_sidebar()
paned.secondary_sidebar = None

root.bind("<space>", controls.toggle_play, add="+")
root.bind("<Command-Left>", controls.previous_track, add="+")
root.bind("<Command-Right>", controls.next_track, add="+")

def check_play_status(selected_view, artist_album=None):
    if selected_view and artist_album:
        return
    else:
        for track in playlist_display.playlist_tree.get_children():
            item = playlist_display.playlist_tree.item(track)
            filepath = item["values"][0]

            if filepath == str(controls.track):
                if player.is_playing():
                    playlist_display.play_status_icon_playing(item["values"][1])
                else:
                    playlist_display.play_status_icon_paused(item["values"][1])

def on_sidebar_selection(event):
    selected_view = sidebar.selected_view
    check_play_status(selected_view)

    if selected_view == "Library" or selected_view == "Songs":
        playlist_display.set_playlist(library)
        check_play_status(selected_view)

    if selected_view == "Favorites":
        playlist_display.show_favorites()
        check_play_status(selected_view)

    if selected_view in playlist_manager.user_playlists.keys():
        user_playlist = playlist_manager.user_playlists[selected_view]
        playlist_display.set_playlist(user_playlist)
        check_play_status(selected_view)

    if selected_view not in ("Artists", "Albums"):
        if paned.secondary_sidebar is not None:
            paned.forget(secondary_sidebar_region)
            paned.secondary_sidebar.destroy()
            paned.secondary_sidebar = None
        return

    if secondary_sidebar_region not in paned.panes():
        paned.insert(1, secondary_sidebar_region)

    if paned.secondary_sidebar is not None:
        paned.secondary_sidebar.destroy()
        paned.secondary_sidebar = None
    
    if selected_view == "Artists":
        playlist_display.clear_playlist()
        items = playlist_display.get_all_artists(library.track_list)
        check_play_status(selected_view)
    else:
        playlist_display.clear_playlist()
        items = playlist_display.get_all_albums(library.track_list)
        check_play_status(selected_view)

    paned.secondary_sidebar = SecondarySidebar(
        secondary_sidebar_region,
        items
    )
    paned.secondary_sidebar.pack(fill="both", expand=True)
    paned.secondary_sidebar.bind("<<SecondarySidebarSelection>>", on_secondary_sidebar_selection)


def on_secondary_sidebar_selection(event):
    sidebar_widget = event.widget
    artist_album = sidebar_widget.selected_view

    if sidebar.selected_view == "Artists" and artist_album:
        playlist_display.set_playlist(library)
        playlist_display.get_artist_tracks(artist_album)
        
    elif sidebar.selected_view == "Albums" and artist_album:
        playlist_display.set_playlist(library)
        playlist_display.get_album_tracks(artist_album)

    controls.check_play_status()

sidebar.bind("<<SidebarSelection>>", on_sidebar_selection)

def play_selected_tracks(event):
    track_values = playlist_display.get_selected_tracks()
    
    selection = playlist_display.playlist_tree.identify_region(event.x, event.y)
    if selection == "heading" or selection == "nothing":
        return

    if track_values is not None:
        controls.playlist = playlist_display.playlist
        controls.update_play_order()
        iid = track_values["index"]
        controls.play_selection(iid)

playlist_display.playlist_tree.bind('<Double-Button-1>', play_selected_tracks)

def on_playlist_created(event):
    display = event.widget
    playlist = display._last_playlist_created
    sidebar.add_user_playlist(playlist)
    playlist_display._set_popup_playlist_list()
    playlist_manager.save_playlists()

playlist_display.bind("<<PlaylistCreated>>", on_playlist_created)

def lock_sidebar():
    try:
        paned.sashpos(0, 200)
    except tk.TclError:
        pass
    root.after(500, lock_sidebar)
root.after(200, lock_sidebar)


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

def volume_up(event):
    volume  = player.player.audio_get_volume()
    if volume <= 95:
        set_audio_volume(volume + 5)
        volume_slider.set(volume + 5)
        return "break"
    else:
        set_audio_volume(100)
        volume_slider.set(100)
        return "break"

def volume_down(event):
    volume = player.player.audio_get_volume()
    if volume >= 5:
        set_audio_volume(volume - 5)
        volume_slider.set(volume -5)
        return "break"
    else:
        set_audio_volume(0)
        volume_slider.set(0)
        return "break"

volume_slider = ttk.Scale(
        top_row_1,
        orient="horizontal",
        from_=0,
        to=100,
        command=set_audio_volume,
        length = 100
    )
volume_slider.set(80)
volume_slider.pack(padx=100, pady=10)

root.bind_all("<Command-Up>", volume_up, add="+")
root.bind_all("<Command-Down>", volume_down, add="+")
playlist_display.playlist_tree.bind("<Command-Up>", volume_up, add="+")
playlist_display.playlist_tree.bind("<Command-Down>", volume_down, add="+")


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

# test_function()
update_time_and_progress()
root.mainloop()