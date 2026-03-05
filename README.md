# Python VLC Music Player

![Python](https://img.shields.io/badge/python-3.x-blue)
![Tkinter](https://img.shields.io/badge/gui-tkinter-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

This is a music player app similar to Apple Music or VLC and is my first personal project for my Boot.dev course. This app is built on the tkinter and VLC libraries. 


<img width="1512" height="662" alt="Screenshot 2026-02-26 at 11 41 22 AM" src="https://github.com/user-attachments/assets/2b0ef793-e198-47da-bffe-83d180b9c210" />


## Built With
  * tkinter
  * python-vlc

## Features
* Plays following audio types: .mp3, .wav, .aac, .flac, .wma, ac3
* Create, save, and delete custom user playlists
* Seamlessly change states - Shuffle, Loop Playlist, Loop Track
* Clickable progress bar allows you change playback position
* Add songs to your favorites list
* Easily see total playlist time

# Setup

### 1. Clone the repository

```bash
git clone https://github.com/alecmstockman/music-player.git
cd music-player
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

macOS / Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

You must also have **VLC installed** on your system since playback is handled through the VLC engine.

---

# Running the App

Start the application with:

```bash
python3 main.py
```

---

# Project Structure

```
music-player/
│
├── main.py                # Application entry point
├── README.md
│
├── src/
│   ├── config.py
│   ├── player_controls.py
│   ├── playlist.py
│   ├── playlist_display.py
│   ├── sidebar.py
│   ├── styles.py
│   └── vlc_player.py
│
├── data/                  # JSON data files (favorites, playlists, etc.)
│
├── Music/
│   ├── Songs/
│   └── Albums/
│
└── venv/                  # Python virtual environment (ignored by git)
```

---

# Current Features

- Playlist view using **Tkinter Treeview**
- Sortable columns
- Favorite tracks
- Playlist creation
- Context menu actions
- VLC-based audio playback
- Sidebar library navigation

---

# Notes

Music files are **not stored in the repository**.  
Place your music files inside:

```
Music/Songs/
Music/Albums/
```

The project uses `.gitkeep` files so these directories exist even when empty.

## Planned Features
* Updates to controls, hotkeys, and right clicks
* Move top control banner to a tkinter grid for cleaner look
* Add ability to sort columns
* Add artwork Display
* Update UI with CustomTkinter
* Create popup play queue and history display
* Implement a play counts column
* Ability to write meta-data to song files
* Ability to change theme and styles
* Recently Played Playlist




    
