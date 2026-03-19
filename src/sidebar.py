import tkinter as tk
from tkinter import ttk
import time
import vlc
from pathlib import Path
from .playlist import Playlist, PlaylistManager
from .vlc_player import VLCPlayer

class Sidebar(ttk.Frame):
    def __init__(self, parent, library, playlist_manager):
        super().__init__(parent)
        self.library = library
        self.parent = parent
        self.playlist = None
        self.playlist_manager = playlist_manager
        self.selected_view = None
        self.library_id = None

        self.playlist_id = None
        self.selected_user_playlist = None

        self.sidebar_tree = ttk.Treeview(self)
        self.popup_menu = tk.Menu(self, tearoff=False)

        self.sidebar_tree.pack(side="left", fill="both", expand=True)
        self.sidebar_tree.column("#0", width=200, stretch=False)
        self.sidebar_tree.heading("#0", text="")
        self.sidebar_tree.bind("<<TreeviewSelect>>", self.on_sidebar_click)
        self.sidebar_tree.bind("<Button-2>", self.on_right_click)
        self.sidebar_tree.bind("<Control-Button-1>", self.on_right_click)
        
        self.sidebar_tree.bind("<<TreeviewOpen>>", self.lock_parents)
        self.sidebar_tree.bind("<<TreeviewClose>>", self.lock_parents)
        


    def set_sidebar(self):
        self.library_id = self.sidebar_tree.insert("", "end", text="Library", values=("Library"), open=True)
        self.playlist_id = self.sidebar_tree.insert("", "end", text="Playlists", values=("Playlists"))

        self.locked_parents = [self.library_id, self.playlist_id]
        for iid in self.locked_parents:
            self.sidebar_tree.item(iid, open=True)
        
        self.sidebar_tree.insert(self.library_id, "end", text="Artists", values=("Artists", ))
        self.sidebar_tree.insert(self.library_id, "end", text="Albums", values=("Albums", ))
        self.sidebar_tree.insert(self.library_id, "end", text="Songs", values=("Songs", ))
        self.sidebar_tree.insert(self.library_id, "end", text="Favorites", values=("Favorites", ))

        self.sidebar_tree.insert(self.playlist_id, "end", text="All Playlists", values=("All Playlists"))
        
        self.popup_menu.add_command(label="Delete Playlist", command=self.delete_user_playlist)

        self.sidebar_tree.item(self.library_id, open=True)
        self.sidebar_tree.item(self.playlist_id, open=True)

        self.set_user_playlists()

    def set_user_playlists(self):
        children = self.sidebar_tree.get_children(self.playlist_id)
        for child in children[1:]:
            self.sidebar_tree.delete(child)

        for key, value in self.playlist_manager.user_playlists.items():
            self.sidebar_tree.insert(self.playlist_id, "end", iid=value.id, text=f"- {value.name}", values=(value.id, value.name))
        
        children = self.sidebar_tree.get_children(self.playlist_id)

    def lock_parents(self, event=None):
        for iid in self.locked_parents:
            if iid in self.sidebar_tree.get_children():
                self.sidebar_tree.item(iid, open=True)

    def on_sidebar_key(self, event):
        if event.keysym == "space":
            selection = self.sidebar_tree.selection()
            for iid in selection:
                if iid in self.locked_parents:
                    return "break"

    def on_sidebar_click(self, event):
        selection = self.sidebar_tree.selection()
        if not selection:
            return
        self.selected_iid = selection[0]
        self.selected_view = self.sidebar_tree.item(self.selected_iid, "values")[0]
        self.event_generate("<<SidebarSelection>>")

    def on_right_click(self, event):
        offset_x = 5
        row_id = self.sidebar_tree.identify_row(event.y)
        
        if row_id in self.playlist_manager.user_playlists:
            self.popup_menu.unpost()
            self.selected_user_playlist = row_id
            try: 
                self.popup_menu.tk_popup(event.x_root + offset_x, event.y_root)
            finally: 
                self.popup_menu.grab_release()

    def set_popup_playlist_list(self):
        for key, value in self.playlist_manager.user_playlists.items():
            self.playlist_submenu.add_command(
                label=f"{value.name}", 
                command=lambda k=key, n=value.name: 
                    self._on_menu_add_to_playlist(k, n)
            )

    def add_user_playlist(self, playlist):
        if not playlist:
            return
        
        if not self.playlist_id:
            print("Playlist parent not initialized")
            return
        self.sidebar_tree.insert(self.playlist_id, "end", iid=playlist.id, text=f"- {playlist.name}", values=(playlist.id, playlist.name))
        
    def delete_user_playlist(self):
        playlist_id = self.selected_user_playlist
        self.playlist_manager.delete_user_playlist(playlist_id)
        self.set_user_playlists()


class SecondarySidebar(ttk.Frame):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)
        self.populate(items)
        self.selected_view = None
        self.tree.bind("<<TreeviewSelect>>", self.on_secondary_sidebar_click)

    def populate(self, items):
        for i, item in enumerate(items):
            self.tree.insert("", "end", iid=str(i), text=item, values=(item, ))

    def on_secondary_sidebar_click(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_iid = selection[0]
        self.selected_view = self.tree.item(self.selected_iid, "values")[0]
        self.event_generate("<<SecondarySidebarSelection>>")
