import tkinter as tk
from tkinter import ttk
import time
import vlc
from src.top_banner import PlayerControls
from src.vlc_player import VLCPlayer
from src.styles import setup_styles
from src.playlist import songs_view


def play():
    player.play()

def pause():
    player.pause()

def next_track():
    print("next")

def previous_track():
    print("previous")


root = tk.Tk()
root.lift()
root.focus_force()
root.title("No Vibe Music Player")
# root.geometry("1000x800")
# root.state('zoomed')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

setup_styles(root)

top_region = ttk.Frame(root)
top_region.pack(side="top", fill="x")
content_region = ttk.Frame(root)
content_region.pack(side="top", fill="both", expand=True)
player = VLCPlayer()

controls = PlayerControls(parent=top_region, player=player)
controls.pack(side="left")

player.load("Music/Songs/01 - BETTER HELL (Thicc boi) [Explicit].mp3")

time_label = tk.Label(content_region, text="00:00 / 00:00", font=("Trebuchet MS", 15), fg="black", bg="gray")
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

songs_view()
update_time_and_progress()
root.mainloop()