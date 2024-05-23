import os
import argparse
from fulldl import download, VERSE_MAP
import random

langs = ['german', 'english']
lang_map = {
  'german': 'Frank Bubenheim',
  'english': 'Al-Hilali', 
}

def get_lang_beautiful():
  # get enumerator for langs
  b = '('
  for i, lang in enumerate(langs):
      r = f'{i}: {lang}'
      if i != len(langs) - 1:
          r += ', '
      b += r
  b += ')'
  return b

def _change_cwd_to_script_location():
  os.chdir(os.path.dirname(os.path.realpath(__file__)))

_change_cwd_to_script_location()

def _exists(path):
  return os.path.exists(path)


parser = argparse.ArgumentParser(description='quickquran - A simple command line tool to get Quran verses quickly')

parser.add_argument('-vk', '--versekey', type=str, help='Combined surah and verse')
parser.add_argument('-r', '--random', action='store_true', help='Get a random verse')
parser.add_argument('-t', '--translation', type=int, help='Translation language code: ' + get_lang_beautiful())

args = parser.parse_args()


vk = not (args.versekey == '' or args.versekey == None)
r = args.random

verse = -1
surah = -1

if vk:
  surah, verse = args.versekey.split(':')

  if not surah.isdigit() or not verse.isdigit():
    print('Error: Invalid versekey')
    exit()
  
  surah, verse = int(surah), int(verse)
elif r:
  random_surah = random.choice(list(VERSE_MAP.keys()))
  random_verse = random.randint(1, VERSE_MAP[random_surah])
  surah, verse = random_surah, random_verse
else:
  print('Please provide a versekey via -vk or use the -r flag to get a random verse')
  exit()

_lang_code = 0 if args.translation == None else args.translation
lang_name = langs[_lang_code]

if not _exists(lang_name):
  download(lang_name, lang_map)

if verse == -1 or surah == -1 or lang_name == '':
  print('Error: Invalid versekey')
  exit() 

target_verse = ''

def get_verse_from_files():
  with open(lang_name + '/' + str(surah) + '.txt', 'r') as f:
    lines = f.readlines()
    return lines[int(verse) - 1]

# try to open file, on error, download the files and retry
try:
  target_verse = get_verse_from_files()
except FileNotFoundError:
  download(lang_name, lang_map)
  # retry
  target_verse = get_verse_from_files()

if target_verse == '':
  print('Error: Verse not found in files')
  exit()

def beautiful_print(x, surah, verse):
  def remove_footnote(x):
    letters = ''
    tag_count = 0
    in_tag = False
    for i in x:
      if i == '<' and tag_count == 0:
        tag_count = 1
        in_tag = True
        continue

      if i == '>' and tag_count == 1:
        tag_count = 2
        continue

      if i == '>' and tag_count == 2:
        in_tag = False
        tag_count = 0
        continue

      if not in_tag:
        letters += i

    return letters
  
  
  if '<' in x:
    x = remove_footnote(x)

  print('\033[96m\n' + x + '\n\033[94m[' + surah + ':' + verse + ']\n')


beautiful_print(target_verse, str(surah), str(verse))