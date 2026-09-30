import argparse
import re
import shutil

import requests


def get_track(artist: str, song: str, session: requests.Session) -> str:
    response = session.get(
        "https://lrclib.net/api/get",
        params={
            "track_name": song,
            "artist_name": artist,
        },
        timeout=10,
    )

    try:
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError("Unable to retrieve lyrics.") from exc

    json_content = response.json()

    return {
        "artist": json_content.get("artistName"),
        "name": json_content.get("trackName"),
        "lyrics": json_content.get("plainLyrics"),
    }


def center_text(text: str) -> str:
    columns = shutil.get_terminal_size().columns

    lines = []
    for line in text.splitlines():
        padding = max(0, (columns - len(line)) // 2)
        lines.append(" " * padding + line)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artist")
    parser.add_argument("song")
    args = parser.parse_args()

    with requests.Session() as session:
        session.headers["User-Agent"] = "lyricfinder/2026"
        track = get_track(args.artist, args.song, session)

    lyrics = (
        f"{track['artist']}\n"
        f"{track['name']}\n\n"
        f"{track['lyrics']}"
    )
    print(center_text(lyrics))

if __name__ == "__main__":
    main()
