import tkinter as tk
from tkinter import ttk

class TrackInfo(tk.Toplevel):
    def __init__(self, parent, track):
        super().__init__(parent)
        self.track = track

        self.title("Track Information")

        self.minsize(500, 450)

        self.transient(parent)   # stay on top of parent
        self.grab_set()          # modal
        self.focus_force()

        self.center_over_parent(parent)

        ttk.Label(self, text="Track Information").pack(anchor="w")

        self.info_tree = ttk.Treeview(
            self,
            columns=("field", "data"),
            show="headings"
        )

        self.info_tree.column("field", width=100, anchor="w")
        self.info_tree.column("data", width=400, anchor="w")

        self.info_tree.heading("field", text="Field")
        self.info_tree.heading("data", text="Value")

        self.info_tree.pack(fill="both", expand=True)

        self.set_fields_and_data()

        self.after(10, lambda: self.center_over_parent(parent))

    def set_fields_and_data(self):
        for field, data in vars(self.track).items():
            self.info_tree.insert("", "end", values=(field, data))

    def center_over_parent(self, parent):
        parent.update_idletasks()
        self.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        win_w = self.winfo_reqwidth()
        win_h = self.winfo_reqheight()

        x = parent_x + (parent_w // 2) - (win_w // 2) - 100
        y = parent_y + (parent_h // 2) - (win_h // 2) - 200

        self.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.lift()
        self.focus_force()
