from .playlist import Track
from mutagen import File
from pathlib import Path
import uuid


def load_track_metadata(filepath):
    track_metadata = {}
    audio = File(filepath, easy=True)
    
    track_metadata["filepath"] = filepath
    track_metadata["id"] = uuid.uuid4().hex[:8]
    track_metadata["title"] = audio.get("title", [filepath.stem])[0]
    track_metadata["artist"] = audio.get("artist", ["Unknown Artist"])[0]
    track_metadata["album"] = audio.get("album", ["Unkown Album"])[0]
    track_metadata["length"] = int(audio.info.length)

    track_metadata["composer"] = audio.get("composer", ["Unknown Composer"])[0]
    track_metadata["copyright"] = audio.get("copyright", ["No Copyright"])[0]
    track_metadata["albumartist"] = audio.get("albumartist", ["No Album Artist"])[0]
    track_metadata["conductor"] = audio.get("conductor", ["No Conductor"])[0]
    track_metadata["discnumber"] = audio.get("discnumber", ["No Disc Number"])[0]
    track_metadata["tracknumber"] = audio.get("tracknumber", ["No Track Number"])[0]
    track_metadata["genre"] = audio.get("genre", ["No Genre"])[0]
    track_metadata["date"] = audio.get("date", ["No Date"])[0]

    track_metadata["sample_rate"] = getattr(audio.info, "sample_rate", "N/A")
    track_metadata["bit_rate"] = getattr(audio.info, "bitrate", "N/A")
    track_metadata["channels"] = getattr(audio.info, "channels", "N/A")
    track_metadata["codec"] = Path(filepath).suffix.lower().strip(".")

    return track_metadata

