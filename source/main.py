import argparse
from bs4 import BeautifulSoup
from os import get_terminal_size
import re
import requests

def format_lyrics(lyrics: str):
  ''' Remove tags and whitespace. '''
  lyrics = re.findall(r'(^[^<]+)', lyrics)
  lyrics = ''.join([line for line in lyrics]).strip()
  return termcenter(lyrics)

def get_lyrics(artist, song):
  ''' Scrapes AZLyrics to get lyrics. '''
  artist, song = artist.replace(' ', ''), song.replace(' ', '')
  url = f'https://www.azlyrics.com/lyrics/{artist}/{song}.html'
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # locate lyrics
    textsoup = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
    lyrics = textsoup.find('div', class_=None).text
    return format_lyrics(lyrics)
  except:
    raise EOFError('Song not found.')

def termcenter(text):
  ''' Centers text-output. '''
  width = get_terminal_size(0).columns
  midtext = ''
  for line in text.split('\n'):
    remainder = width - len(line)
    spaces = round(remainder/2)
    midtext += ' '*spaces + line + '\n'
  return midtext

def main():
  # parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("artist")
  parser.add_argument("song")
  args = parser.parse_args()
  # print lyrics
  print(get_lyrics(args.artist, args.song))

if __name__ == "__main__":
  main()
