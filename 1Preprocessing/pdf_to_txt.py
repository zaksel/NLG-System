#Script parses and processes PDF Files of an Directory and saves them in a textfile
import re
from tika import parser
import os, tqdm

pdf_dir = "./data/training/PDF" #folder to Trainingdata
output_dir = "./data/training/TXT"

num_words = 0
num_chars = 0
paths = []


for (dirpath, _, file_names) in os.walk(pdf_dir):
    for file in file_names:
        paths.append(os.path.join(dirpath, file))

for path in tqdm.tqdm(paths):
    with open(os.path.join(output_dir, os.path.basename(path)[:-4]+".txt"), 'w+', encoding='utf-8', errors="strict") as f:
        text = parser.from_file(path)['content']

        #text = re.sub(".{17,}", "", text)  # delete long char-rows (>16) like links or delimiters (longest german wors are around 34 words see: Donau-Dampfschifffahrtsgesellschaft)
        text = text.replace('-\n', '').replace('\n', ' ').replace('\r', ' ').replace('\0', ' ').replace('\t',' ').replace('..', ' ').replace('. .', ' ')  # replace everything we dont want with whitespace
        text = re.sub("[ ]{2,}", " ", text)  # eliminate double or more whitespaces

        # split on whitespaces and process word by word
        text = text.split(" ")
        text_clean = []
        for i in range(0, len(text)):
            if all(31 < ord(char) < 127 for char in text[i]):   # Regex [ -~]
                text_clean.append(text[i])
        text = " ".join(text_clean)

        # text = text.split(" ")
        # i = 0
        # while i < len(text)-1:
        #     token = text[i]
        #     if len(token) < 4 and len(text[i+1]) < 4:
        #         text.pop(i)
        #     elif len(token) > 24:
        #         text.pop(i)
        #     else:
        #         for char in token:
        #             if ord(char) < 32 or ord(char) > 126:   # Regex [ -~]
        #                 text.pop(i)
        #                 break
        #     i += 1
        # text = ' '.join(text)

        num_chars = num_chars+len(text)
        num_words = num_words + len(text.split(" "))
        print(text+" ", file=f, end='')
        f.close()

print("All PDFs from " + pdf_dir + " parsed to " + output_dir)
print("Stats:\nNumber of Chars: ", num_chars ,"\nNumber of Words: ", num_words)

