import os

# change cwd to the script location
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# in english folder, get all file contents in a map
#               key: surah number      value: another map
# another map:  key: verse number      value: verse text
def get_english_map():
  english_map = {}
  for filename in os.listdir('english'):
    with open('english/' + filename, 'r') as f:
      lines = f.readlines()
      surah = int(filename.split('.')[0])
      verse_map = {}
      for i, line in enumerate(lines):
        verse_map[i + 1] = line
      english_map[surah] = verse_map
  return english_map

english_map = get_english_map()

# function to get arabic substring from a string

def get_arabic_substring(text):
  arabic_substring = ''
  last_space = False
  for c in text:
    if '\u0600' <= c <= '\u06FF':
      arabic_substring += c
      last_space = False
    else:
      arabic_substring += '-' if not last_space else ' '
      last_space = True

  # all whitespace chunks > 1 will be replaced with a single whitespace
  arabic_substring = arabic_substring.split()[1:]
  arabic_substring = [x[:-1].replace('-', ' ') for x in arabic_substring]

  return arabic_substring

# print all
arabic_words = []

for surah, verses in english_map.items():
  for verse, text in verses.items():
    # check if it has a substring that has arabic letters
    if any(c for c in text if '\u0600' <= c <= '\u06FF'):
      # print arabic substring
      arabic = get_arabic_substring(text)
      for a in arabic:
        if a not in arabic_words:
          arabic_words.append(a)

print(arabic_words)
print()

for a in arabic_words:
  print(a)
  print()

'''
صلى الله عليه وسلم
ṣallā-llāhu 3alayhi wa sallam

كبش
kabš

صلى الله عليه و سلم
ṣallā-llāhu ʿalayhi wa-sallam

عليهما السلام
ʿalayhīma-s-salām

رضي الله عنهما
raḍiya-llāhu ʿanhā

يوشع وكالب
Yūša wa Kālab

رضي الله عنه
raḍiya-llāhu ʿanhu

رضي الله عنهم
raḍiya-llāhu ʿanhum

عليه السلام
ʿalayhi-s-salām

جل جلاله

السلام عليهما

عز وجل

توحيد الله

عليهم السلام

تاخذ اجرا

تعالى

رضي الله عنها

السلام عليكم

القضاء والقدر

السيد الذي يصمد إليه في الحاجات

الإيمان بالقدر

الظهار
'''