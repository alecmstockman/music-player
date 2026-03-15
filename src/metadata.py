from .playlist import Track
from mutagen import File


def load_track_metadata(filepath):
    audio = File(filepath, easy=True)
    track_list = {}

    title = audio.get("title", [filepath])[0]
    artist = audio.get("artist", ["Unknown Artist"])[0]
    album = audio.get("album", ["Unkown Album"])[0]
    composer = audio.get("composer", ["Unkown composer"])[0]
    track_copyright  = audio.get("copyright", ["No Copyright"])[0]
    albumartist = audio.get("albumartist", ["No Album Artist"])[0]
    conductor = audio.get("conductor", ["No Conductor"])[0]
    discnumber = audio.get("discnumber", ["No Disc Number"])[0]
    tracknumber = audio.get("tracknumber", ["No Track Number"])[0]
    genre = audio.get("genre", ["No Genre"])[0]
    date = audio.get("date", ["No Date"])[0]

    length = audio.info.length
    sample_rate = audio.info.sample_rate
    meta_data = [title, artist, album, composer, track_copyright, albumartist, conductor, discnumber, tracknumber, genre, date]

    print(int(length), sample_rate)
    print("------------------")
    for item in audio:
        track_list[item] = audio.get(f"{item}", ["None"])[0]

    print("track_list:")
    print(track_list)

