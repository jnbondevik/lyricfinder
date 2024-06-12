from selenium import webdriver
from selenium.webdriver.common.by import By
import argparse

def format_arguments(artist: str, song: str):
  return artist.lower(), song.replace(" ", "").lower()

def format_lyrics(lyrics: str):
  # remove comment
  lyrics = "".join(lyrics.split("-->")[1:])
  # remove <br>
  lyrics = lyrics.replace(r"<br>", "")
  return lyrics

def get_lyrics(artist, song):
  op = webdriver.ChromeOptions()
  op.add_argument("headless")
  driver = webdriver.Chrome(options=op)
  driver.get(f"https://www.azlyrics.com/lyrics/{artist}/{song}.html")
  try:
    # find parent node of comment before the song lyrics
    lyrics = driver.find_element(By.XPATH, "//comment()[contains(., 'azlyrics.com content by')]/..")
    # get the HTML
    lyrics = lyrics.get_attribute("innerHTML")
    lyrics = format_lyrics(lyrics)
  except Exception:
    print("Lyrics not found! Check name.")
    lyrics = None
  finally:
    driver.close()
  return lyrics

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("artist", help="The artist name.")
  parser.add_argument("song", help="The song name.")
  args = parser.parse_args()
  artist, song = format_arguments(args.artist, args.song)
  lyrics = get_lyrics(artist, song)
  if lyrics:
    f = open(f"{artist}-{song}-lyrics", "w")
    f.write(lyrics)
    f.close()
    return 0
  else:
    return 1

if __name__ == "__main__":
  main()