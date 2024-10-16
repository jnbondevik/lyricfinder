import argparse
from importlib import resources
from os import get_terminal_size
import requests

def parse_args() -> dict:
  ''' Retrieve command line arguments as a dict. '''
  parser = argparse.ArgumentParser()
  parser.add_argument("artist")
  parser.add_argument("song")
  return vars(parser.parse_args())

def get_api(path: str) -> str:
  # Get path after pip install
  with resources.open_text('source', 'apikey') as file:
  # with open(path) as file:
    for line in file.readlines():
      if not line.startswith(('#', '\n')):
        return line
  raise FileNotFoundError('Please provide API-key to source/apikey before installation.')
      
def termcenter(text):
  ''' Centers text-output. '''
  width = get_terminal_size(0).columns
  midtext = ''
  for line in text.split('\n'):
    remainder = width - len(line)
    spaces = round(remainder/2)
    midtext += ' '*spaces + line + '\n'
  return midtext

def get_lyrics(artist, song):
  ''' Calls the MusixMatch API to retrieve lyrics. '''
  params = {
    'q_track': song, 'q_artist': artist, 
    'apikey': get_api('source/apikey')
    }
  url = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get'
  response = requests.get(url, params=params).json()
  status = response['message']['header']['status_code']
  if  status != 200:
    raise requests.HTTPError('Song not found.')
  lyrics = response['message']['body']['lyrics']['lyrics_body']
  return lyrics

def main():
  args = parse_args() # get artist and song
  print(
    termcenter(get_lyrics(args['artist'], args['song']))
    ) # print to stdout

if __name__ == "__main__":
  main()
