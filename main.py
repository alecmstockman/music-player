import tkinter as tk
from tkinter import ttk
import vlc
from pathlib import Path
from src.player_controls import PlayerControls
from src.track_display import TrackDisplay
from src.vlc_player import VLCPlayer
from src.playlist import PlaylistManager, Library
from src.styles import setup_styles
from src.playlist_display import PlaylistDisplay
from src.sidebar import Sidebar, SecondarySidebar

root = tk.Tk()
root.lift()
root.focus_force()
root.title("No Vibe Music Player - VERSION 2")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(800, 600)

top_region = ttk.Frame(root, style="Border.TFrame")
top_region.grid(row=0, column=0, sticky="ew")
root.columnconfigure(0, weight=1)

top_region.columnconfigure(0, weight=0, minsize=250)
top_region.columnconfigure(1, weight=1, minsize=300)
top_region.columnconfigure(2, weight=0, minsize=100)

left_controls = ttk.Frame(top_region)
center_display = ttk.Frame(top_region)
right_controls = ttk.Frame(top_region)

left_controls.grid(row=0, column=0, sticky="w", padx=10)
center_display.grid(row=0, column=1, sticky="ew")
right_controls.grid(row=0, column=2, sticky="e", padx=10)

paned = ttk.PanedWindow(root, orient="horizontal")
paned.grid(row=1, column=0, sticky="nsew")
root.rowconfigure(1, weight=1)

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

library = Library()
library.load_library()




album_dir = p / "albums"
album_dir_list = [filename for filename in album_dir.iterdir() if filename.is_dir()]

playlist_manager = PlaylistManager(library)
playlist_manager.create_library_playlist()
playlist_manager.update_favorites_playlist()

track_display = TrackDisplay(center_display, library, player)
track_display.pack(fill="x", expand=True)
track_display.update_time_and_progress()

playlist_display = PlaylistDisplay(playlist_display_region, library, player, library, playlist_manager)
playlist_display.pack(fill="both", expand=True)
playlist_display.set_playlist(playlist_manager.library_playlist)

controls = PlayerControls(left_controls, library, playlist_manager.library_playlist, player, track_display, playlist_display)
controls.pack(side="left")
playlist_display.controls = controls

first_track_id = controls.playlist.track_id_list[controls.play_index]
first_track = library.get_track(first_track_id)
player.load(Path(first_track.filepath))

playlist_manager.load_playlist()
playlist_display._set_popup_playlist_list()

sidebar = Sidebar(sidebar_region, library, playlist_manager)
sidebar.pack(fill="both", expand=True)
sidebar.set_sidebar()
paned.secondary_sidebar = None

def on_left_button_previous(event):
    controls.previous_track()

def on_right_button_next(event):
    controls.next_track()

root.bind("<space>", controls.toggle_play, add="+")
root.bind("<Command-Left>", controls.previous_track, add="+")
root.bind("<Command-Right>", controls.next_track, add="+")

def check_play_status(selected_view, artist_album=None):
    print("MAIN - CHECK PLAY STATUS")
    if selected_view and artist_album:
        print("main, check_play_status err: selected view and artist_album")
        return
    else:
        track = library.tracks[controls.track]
        if player.is_playing():
            playlist_display.play_status_icon_playing(track.track_id)
        else:
            playlist_display.play_status_icon_paused(track.track_id)

def on_sidebar_selection(event):
    print("\nON SIDEBAR SELECTION")
    selected_view = sidebar.selected_view
    print(f"Selected view: {selected_view}")
    if selected_view == "Library" or selected_view == "Songs":
        playlist_display.set_playlist(playlist_manager.library_playlist)
        check_play_status(selected_view)

    if selected_view == "Favorites":
        playlist_display.set_playlist(playlist_manager.favorites_playlist)
        check_play_status(selected_view)

    if selected_view in playlist_manager.user_playlists.keys():
        print(f"-Sected view: {selected_view}")
        user_playlist = playlist_manager.user_playlists[selected_view]
        print(f"-User Playlist: {user_playlist}")
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
        items = playlist_display.get_all_artists()
        check_play_status(selected_view)
    else:
        playlist_display.clear_playlist()
        items = playlist_display.get_all_albums()
        check_play_status(selected_view)

    paned.secondary_sidebar = SecondarySidebar(
        secondary_sidebar_region,
        items
    )
    paned.secondary_sidebar.pack(fill="both", expand=True)
    paned.secondary_sidebar.bind("<<SecondarySidebarSelection>>", on_secondary_sidebar_selection)


def on_secondary_sidebar_selection(event):
    print("\nMAIN: on_secondary_sidebar_selection")
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
    print("\nMAIN: play_selected_tracks")
    selection = playlist_display.playlist_tree.identify_region(event.x, event.y)
    if selection == "heading" or selection == "nothing":
        return
    
    track_values = playlist_display.get_selected_tracks()

    if track_values is not None:
        controls.playlist = playlist_display.playlist
        controls.update_play_order() 
        controls.play_selection(track_values["track_id"])
        track_display.update_track_display(track_values["track_id"])

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
        right_controls,
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
    for song in library.tracks:
        print(f"{count}: {song}")
        count += 1
    print("\n")

# print(load_track_metadata("Music/Songs/08 Just Pretend.mp3"))

# test_function()
track_display.update_time_and_progress()
root.mainloop()