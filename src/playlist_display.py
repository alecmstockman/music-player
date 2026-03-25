import tkinter as tk
from tkinter import ttk
import vlc
from pathlib import Path
from src.playlist import Playlist, PlaylistManager, CreatePlaylistEntry
from src.track_info import TrackInfo


class PlaylistDisplay(ttk.Frame):
    def __init__(self, parent, library, player, playlist, playlist_manager):
        super().__init__(parent)
        self.library = library
        self.player = player
        self.playlist = playlist
        self.playlist_manager = playlist_manager
        
        self.popup_menu = tk.Menu(self, tearoff=False)
        self.playlist_submenu = tk.Menu(self.popup_menu, tearoff=False)
        self.menu_iid = None
        # self.favorites = {}
        # self.load_favorites()
        self._last_playlist_created = None
        self.sort_order = None
        # self.backup_list = self.playlist.track_list.copy()

        self.header_var = tk.StringVar()
        self.header_var.set(playlist.name)
        
        self.display_header = tk.Frame(self, bg="#2b2b2b", height=40)
        self.display_header.pack(fill="x")

        self.header_label = tk.Label(
            self.display_header,
            textvariable=self.header_var,
            font=("Trebuchet MS", 16),
            fg="white",
            bg="#1d1d1d",
            anchor="w",       
            padx=10
        )
        self.header_label.pack(fill="both", expand=True)
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        self.playlist_tree = ttk.Treeview(
            self, 
            columns=("filepath", "track_id", "index", "play status", "Track", "Menu", "Time", "Artist", "Album", "favorite", "Filetype", "Blank"), 
            show="headings"
        )
        self.playlist_tree.pack(side="left", fill="both", expand=True)
        
        self.playlist_tree.column("filepath", width=0, stretch=False)
        self.playlist_tree.column("track_id", width=0, stretch=False)
        self.playlist_tree.column("index", width=0, stretch=False)
        self.playlist_tree.column("play status", anchor="w", width=40, stretch=False)
        self.playlist_tree.column("Track", anchor="w", width=400, stretch=False)
        self.playlist_tree.column("Menu", anchor="e", width=20, stretch=False)
        self.playlist_tree.column("Time", anchor="e", width=60, stretch=False)
        self.playlist_tree.column("Artist", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Album", anchor="w", width=200, stretch=False)
        self.playlist_tree.column("Filetype", anchor="e", width=100, stretch=False)
        self.playlist_tree.column("favorite", anchor="e", width=40, stretch=False)
        self.playlist_tree.column("Blank", anchor="w", width=200, stretch=True)
        
        self.playlist_tree.heading("filepath")
        self.playlist_tree.heading("track_id")
        self.playlist_tree.heading("index")
        self.playlist_tree.heading("play status", text="  ")
        self.playlist_tree.heading("Track", text="  Title  ")
        self.playlist_tree.heading("Menu", text="···")
        self.playlist_tree.heading("Time", text=" Time ")
        self.playlist_tree.heading("Artist", text=" Artist ")
        self.playlist_tree.heading("Album", text="  Album  ")
        self.playlist_tree.heading("favorite", text="  ")
        self.playlist_tree.heading("Filetype", text="  Filetype  ")
        self.playlist_tree.heading("Blank", text="")

        self.playlist_tree.heading("Track", command=lambda: self.sort_column("Track"))
        self.playlist_tree.heading("Time", command=lambda: self.sort_column("Time"))
        self.playlist_tree.heading("Artist", command=lambda: self.sort_column("Artist"))
        self.playlist_tree.heading("Album", command=lambda: self.sort_column("Album"))
        self.playlist_tree.heading("favorite", command=lambda: self.sort_column("favorite"))
        self.playlist_tree.heading("Filetype", command=lambda: self.sort_column("Filetype"))

        self.playlist_tree.bind("<Button-1>", self.on_tree_click)
        self.playlist_tree.bind("<Button-2>", self.on_tree_right_click)

        self.popup_menu.add_command(label="Play", command=self._on_menu_play)
        self.popup_menu.add_command(label="Previous", command=self._on_menu_previous_track)
        self.popup_menu.add_command(label="Next", command=self._on_menu_next_track)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Create Playlist", command=self._on_menu_create_playlist)
        self.popup_menu.add_separator()
        self.popup_menu.add_cascade(label="Add to Playlist", menu=self.playlist_submenu)
        self.popup_menu.add_command(label="Delete from Playlist", command=self._on_menu_delete_from_playlist)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Favorite", command=self._on_menu_update_favorite)
        self.popup_menu.add_command(label="Remove Favorite", command=self._on_menu_update_favorite)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Track Info", command=self.display_track_info)
        self.popup_menu.add_command(label="Write meta-data", command=self._on_menu_update_favorite, state=tk.DISABLED)
        
        self.playlist_tree.tag_configure("playing", background="#476288") 
        self.playlist_tree.bind("<<TreeviewSelect>>", self.on_tree_selection)

    def set_playlist(self, playlist):

        self.playlist = playlist
        self.clear_playlist()

        print(playlist.name)
        if not playlist or not hasattr(playlist, "track_id_list"):
            print("No playlist or invalid playlist object")
            return
        index = 0
        even = True

        for item in self.playlist.track_id_list:
            track = self.library.tracks[item]

            filepath = track.filepath
            track_id = track.track_id
            title = track.title
            artist = track.artist
            album = track.album
            total_s = track.length
            total_str = f"{total_s//60:d}:{total_s%60:02d}"
            filetype = track.codec
            favorite = track.favorite

            self.playlist_tree.tag_configure("even", background="darkblue")
            self.playlist_tree.tag_configure("odd", background="black")

            star = " ★ " if favorite == True else " ☆ "

            track_index = index
            if even is True:
                self.playlist_tree.insert(
                    "", "end",
                    iid=str(track_id),
                    values=("", f"{track_id}", f"{track_index}", "", f"{title}", "···", f"{total_str}", f"{artist}", f"{album}", f"{star}", f"{filetype}"),
                    tags="even" 
                )
                even = False
            else:
                self.playlist_tree.insert(
                    "", "end",
                    iid=str(track_id),
                    values=("", f"{track_id}", f"{track_index}", "", f"{title}", "···", f"{total_str}", f"{artist}", f"{album}", f"{star}", f"{filetype}"),
                    tags="odd" 
                )
                even = True
            index += 1

            if self.playlist.id in self.playlist_manager.user_playlists.keys():
                 self.popup_menu.entryconfig("Delete from Playlist", state="normal")
            else:
                self.popup_menu.entryconfig("Delete from Playlist", state="disabled")
        self.get_playlist_time()

    def get_playlist_time(self):
        self.HEADER_TEXT = self.playlist.name
        children = self.playlist_tree.get_children()
        total_seconds = 0
        
        for child in children:
            item = self.playlist_tree.item(child)["values"]
            time_str = item[6]
            minutes, seconds = map(int, time_str.split(":"))
            total_seconds += minutes * 60 + seconds 

        total_minutes = total_seconds // 60 
        remaining_seconds = total_seconds % 60
        if remaining_seconds <= 9:
            remaining_seconds = f"0{remaining_seconds}"
        if total_minutes >= 60:
            total_hours = total_minutes // 60
            remaining_minutes = total_minutes % 60
            if remaining_minutes <= 9:
                remaining_minutes = f"0{remaining_minutes}"
            self.header_var.set(f"{self.playlist.name} ({total_hours}:{remaining_minutes}:{remaining_seconds})")
        else:
            self.header_var.set(f"{self.playlist.name} ({total_minutes}:{remaining_seconds})")

    def clear_playlist(self):
        for iid in self.playlist_tree.get_children():
            self.playlist_tree.delete(iid)

    def highlight_playing(self, track_id):
        for item in self.playlist_tree.get_children():
            current_tags = list(self.playlist_tree.item(item, "tags"))
            if "playing" in current_tags:
                current_tags.remove("playing")
            self.playlist_tree.item(item, tags=tuple(current_tags))

        current_tags = list(self.playlist_tree.item(track_id, "tags"))
        if "playing" not in current_tags:
            current_tags.append("playing")

        self.playlist_tree.item(track_id, tags=tuple(current_tags))
        self.playlist_tree.see(track_id)

    def get_selected_tracks(self):
        selection = self.playlist_tree.selection()
        first_track_id = selection[0]

        if not selection:
            print("playlist_display: get_selected_tracks, no selection")
            return None
        
        selected_iid = self.playlist_tree.item(first_track_id)

        values = selected_iid["values"]
        return {
            "filepath": values[0],
            "track_id": str(values[1]),
            "index": int(values[2]),
            "play status": values[3],
            "title": str(values[4]),
            "length": values[5],
            "artist": str(values[6]), 
            "album": str(values[7]),
            "filetype": values[8]
        }
    
    def clear_play_status(self):
        for iid in self.playlist_tree.get_children():
            if iid is None:
                return
            self.playlist_tree.set(iid, column="play status", value="")

    # def remove_play_status_icon(self, index):
    #     if index is None:
    #         print("playlist_display: remove_play_status_icon, index is None")
    #         return
    #     iid = index
    #     self.playlist_tree.set(iid, column="play status", value="   ")     

    def play_status_icon_playing(self, track_id):
        if not self.playlist_tree.get_children():
            return
        if track_id is None:
            print("playlist_display: play_status_icon_playing, track_id is None")
            return
        if track_id not in self.playlist.track_id_list:
            print(f"DISPLAY: play_status_icon_playing: {track_id} not in playlist: {self.playlist.name}")
            return
        self.playlist_tree.set(track_id, column="play status", value="  🔊")

    def play_status_icon_paused(self, track_id):
        if not self.playlist_tree.get_children():
            return
        if track_id is None:
            print("playlist_display: play_status_icon_paused, track_id is None")
            return
        if track_id not in self.playlist.track_id_list:
            print(f"DISPLAY: play_status_icon_paused: {track_id} not in playlist: {self.playlist.name}")
            return
        self.playlist_tree.set(track_id, column="play status", value="  🔈")

    def on_tree_selection(self, event):
        selected = self.playlist_tree.selection
        return selected        
    
    def on_tree_click(self, event):
        row_id = self.playlist_tree.identify_row(event.y)
        col_id = self.playlist_tree.identify_column(event.x)

        if not row_id:
            return
        
        self.playlist_tree.selection_set(row_id)            
        self.menu_iid = row_id
        if col_id == "#6":
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        elif col_id == "#10":
            self._update_favorite(row_id)

    def on_tree_right_click(self, event):
        row_id = self.playlist_tree.identify_row(event.y)

        if not row_id:
            return
        
        self.menu_iid = row_id
        self.popup_menu.tk_popup(event.x_root, event.y_root)


    def sort_column(self, column):
        items = [(self.playlist_tree.set(iid, column), iid) for iid in self.playlist_tree.get_children()]
        
        if column in ("Track", "Artist", "Album", "Filetype"):
            if self.sort_order == None:
                items.sort()
                for index, (_, iid) in enumerate(items):
                    self.playlist_tree.move(iid, "", index)
                self.sort_order = "descending"
                if column == "Track":
                    self.playlist_tree.heading(column, text=f"  Title ⬆")
                else:
                    self.playlist_tree.heading(column, text=f"  {column} ⬆")

            elif self.sort_order == "descending":
                items.reverse()
                for index, (_, iid) in enumerate(items):
                    self.playlist_tree.move(iid, "", index)
                self.sort_order = "ascending"
                if column == "Track":
                    self.playlist_tree.heading(column, text=f"  Title ⬇")
                else:
                    self.playlist_tree.heading(column, text=f"  {column} ⬇")

            elif self.sort_order == "ascending":
                self.set_playlist(self.playlist)
                self.sort_order = None
                
                if column == "Track":
                    self.playlist_tree.heading(column, text=f"  Title  ")
                else:
                    self.playlist_tree.heading(column, text=f"  {column}  ")

            self.recolor_rows()
            self.event_generate("<<PlaylistSorted>>")
            return
        
    def get_post_sort_play_order(self):
        children = self.playlist_tree.get_children()
        new_play_order = []
        for child in children:
            track = self.playlist_tree.item(child)
            values = track["values"]
            index = values[2]
            new_play_order.append(index)
        return new_play_order

    def recolor_rows(self):
        for index, iid in enumerate(self.playlist_tree.get_children()):
            if index % 2 == 0:
                self.playlist_tree.item(iid, tags=("even",))
            if index % 2 == 1:
                self.playlist_tree.item(iid, tags=("odd",))

    def _on_menu_play(self):
        self.clear_play_status()
        self.controls.play_index = int(self.menu_iid)
        index = self.controls.play_order[self.controls.play_index]
        track = self.playlist.track_id_list[index]
        self.player.load(track)
        self.player.play()
        self.play_status_icon_playing(index)

    def _on_menu_previous_track(self):
        self.clear_play_status()
        self.controls.play_index = int(self.menu_iid)
        self.controls.previous_track()        

    def _on_menu_next_track(self):
        self.clear_play_status()
        self.controls.play_index = int(self.menu_iid)
        self.controls.next_track()

    def _on_menu_create_playlist(self):
        dialog = CreatePlaylistEntry(self)
        self.wait_window(dialog)
        playlist_name = dialog.result

        if not playlist_name:
            return

        playlist = self.playlist_manager.create_playlist(playlist_name)

        self._last_playlist_created = playlist
        self.event_generate("<<PlaylistCreated>>")

    def _set_popup_playlist_list(self):
        self.playlist_submenu.delete(0, "end")
        for key, value in self.playlist_manager.user_playlists.items():
            self.playlist_submenu.add_command( 
                label=f"{value.name}", 
                command=lambda k=key, n=value.name: 
                    self._on_menu_add_to_playlist(k, n)
            )
    
    def _on_menu_add_to_playlist(self, key, name):
        track = self.playlist_tree.set(self.menu_iid, "track_id")
        self.playlist_manager.add_to_user_playlist(key, track)
        self.menu_iid = None

    def _on_menu_delete_from_playlist(self):
        track = self.playlist_tree.set(self.menu_iid, "track_id")
        new_list = []

        for item in self.playlist.track_id_list:
            if track != str(item):
                new_list.append(item)
        self.playlist.track_id_list = new_list
        
        self.set_playlist(self.playlist)
        self.playlist_manager.update_user_playlist(self.playlist.id)

    def _on_menu_update_favorite(self):
        self._update_favorite(self.menu_iid)
        
    def _update_favorite(self, track_id):
        if track_id is None or not self.playlist_tree.exists(track_id):
            print("playlist_display: _update_favorite, iid is None or doesn't exit")
            return
        
        value = self.playlist_tree.set(track_id, column="favorite")
        track = self.library.tracks[track_id]

        if value == " ☆ ":
            self.playlist_tree.set(track_id, column="favorite", value=" ★ ")
            track.favorite = True
            self.library.tracks[track_id].favorite = True
        elif value == " ★ ":
            self.playlist_tree.set(track_id, column="favorite", value=" ☆ ")
            track.favorite = False

        self.library.save_library()
        self.playlist_manager.update_favorites_playlist()

    def save_favorites(self):
        self.library.save_library()
        self.playlist_manager.update_favorites_playlist()

    def show_favorites(self):
        self.clear_playlist()
        self.set_playlist(self.playlist_manager.favorites_playlist)

    def get_all_artists(self):
        artist_set = set()
        for value in self.library.tracks.values():
            artist = value.artist
            if artist:
                artist_set.add(artist)
        return sorted(artist_set)
    
    def get_all_albums(self):
        album_set = set()
        for value in self.library.tracks.values():
            album = value.album
            if album:
                album_set.add(album)
        return sorted(album_set)
    
    def get_artist_tracks(self, artist_album):
        track_id_list = []
        for track_id in self.library.tracks:
            track = self.library.tracks[track_id]
            if artist_album == track.artist:
                track_id_list.append(track.track_id)

        playlist = Playlist(f"{artist_album} - All Tracks", track_id_list)
        self.set_playlist(playlist)
                
    def get_album_tracks(self, artist_album):
        track_list = []
        for track_id in self.library.tracks:
            track = self.library.tracks[track_id]
            if artist_album == track.album:
                track_list.append(track.track_id)  

        playlist = Playlist(f"{artist_album} - Album Tracks", track_list)
        self.set_playlist(playlist)

    def display_track_info(self):
        selected = self.playlist_tree.selection()
        if not selected:
            return
        
        track_id = self.menu_iid
        track = self.library.tracks[track_id]
        self.track_info_popup = TrackInfo(self, track)


        



