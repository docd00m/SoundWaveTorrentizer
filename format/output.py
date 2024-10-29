def bbcode(metadata):
  bbcode = "[table]\n"
  bbcode += "[tr]\n"
  bbcode += f"[td][b]Filename[/b][/td]\n"

  for key in metadata[list(metadata.keys())[0]]:
    bbcode += f"[td][b]{key.capitalize()}[/b][/td]\n"
  bbcode += "[/tr]\n"

  for track, track_info in metadata.items():
    bbcode += f"[tr]\n[td]{track}[/td]\n"
    for key, value in track_info.items():

      bbcode += f"[td]"
      if key == "spectrogram":
        bbcode += "[url]"
      bbcode += f"{value}"
      if key == "spectrogram":
        bbcode += "[/url]"
      bbcode += "[/td]\n"

    bbcode += "[/tr]\n"

  bbcode += "[/table]"
  return bbcode


def markdown(metadata):
    headers = ["Filename"] + [key.capitalize() for key in metadata[list(metadata.keys())[0]]]
    md_table = "| " + " | ".join(headers) + " |\n"
    
    md_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    for track, track_info in metadata.items():
        row = [track] + list(track_info.values())
        md_table += "| " + " | ".join(row) + " |\n"
    
    return md_table


def bbcode_compact(metadata):
    # TODO: rework metadata so it contains album info instead of pulling summary info from first track.
    # TODO: add albumartist, album, and release date to metadata for a better summary
    first_track = list(metadata.values())[0]
    output = ""
    if "albumartist" in first_track:
        output += "[size=22][b]"
        if "musicbrainz_albumartistid" in first_track:
            output += f"[url=https://musicbrainz.org/artist/{first_track["musicbrainz_albumartistid"]}]"
        output += first_track["albumartist"]
        if "musicbrainz_albumartistid" in first_track:
            output += "[/url]"
        output += "[/b][/size]\n"

    if "album" in first_track:
        output += "[size=22][b]"
        if "musicbrainz_albumid" in first_track:
            output += f"[url=https://musicbrainz.org/release/{first_track['musicbrainz_albumid']}]"
        output += first_track["album"]
        if "musicbrainz_albumid" in first_track:
            output += "[/url]"
        output += "[/b][/size]\n"

    if "date" in first_track:
        output += f"[size=16]{first_track["date"]}[/size]\n"

    output += (f"[size=16]{first_track["codec"]} / {first_track["channels"]} ch / {first_track["bits_per_sample"]} bit"
              f" / {first_track["sample_rate"]}[/size]\n\n[list=1]")

    for track, track_info in metadata.items():
        output += "[*]"
        if track_info["embedded_cuesheet"]:
            output += ":cd:"
        if "spectrogram" in track_info and track_info["spectrogram"] != "N/A":
            output += f" [url={track_info["spectrogram"]}]:bar_chart:[/url]"

        output += (f"{track_info["artist"]} - {track_info["title"]} / {track_info["duration"]} "
                   f"/ {track_info["bitrate"]} / {track_info["audio_md5"]}\n")

    output += ("[/list]\n\n"
               ":cd:: indicates the track contains an embedded cuesheet.\n"
               ":bar_chart:: indicates the track has a spectrogram for it, click the icon to view.\n")
    return output
