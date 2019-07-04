#Script parses and processes PDF Files of an Directory and saves them in a textfile
import re
from tika import parser
import os, tqdm

pdf_dir = "./data/training/PDF" #folder to Trainingdata
output_file = "./data/training/trainingsdaten.txt"

num_words=0
num_chars=0
paths = []


for (dirpath, _, file_names) in os.walk(pdf_dir):
    for file in file_names:
        paths.append(os.path.join(dirpath, file))

with open(output_file, 'a+', encoding='utf-8', errors="strict") as f:
    for path in tqdm.tqdm(paths):
        text = parser.from_file(path)['content']

        #text = re.sub(".{17,}", "", text)  # delete long char-rows (>16) like links or delimiters (longest german wors are around 34 words see: Donau-Dampfschifffahrtsgesellschaft)
        text = text.replace('-\n', '').replace('\n', ' ').replace('\r', ' ').replace('\0', ' ').replace('\t',' ').replace('..', ' ').replace('. .', ' ')  # replace everything we dont want with whitespace
        text = re.sub("[ ]{2,}", " ", text)  # eliminate double or more whitespaces

        num_chars = num_chars+len(text)
        num_words = num_words + len(text.split(" "))
        print(text+" ", file=f, end='')

print("All PDFs from " + pdf_dir + " parsed to " + output_file)
print("Stats:\nNumber of Chars: ", num_chars ,"\nNumber of Words: ", num_words)

