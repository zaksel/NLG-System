import glob
import numpy as np
import os
import tqdm
from tika import parser
import re

def load_dataset(enc, path, combine):
    paths = []
    if os.path.isfile(path):
        # Simple file
        paths.append(path)
    elif os.path.isdir(path):
        # Directory
        for (dirpath, _, fnames) in os.walk(path):
            for fname in fnames:
                paths.append(os.path.join(dirpath, fname))
    else:
        # Assume glob
        paths = glob.glob(path)

    token_chunks = []
    raw_text = ''
    for path in tqdm.tqdm(paths):
        if path.endswith('.npz'):
            # Pre-encoded
            with np.load(path) as npz:
                for item in npz.files:
                    token_chunks.append(npz[item])

        elif path.endswith('.pdf'):
            #PDF-Files
            new_text = parser.from_file(path)['content']
            #new_text = re.sub("\n", "", new_text)
            #new_text.encode("utf-8", "ignore")
            #Only Look for Paragraphs wich have more than para_length tokens
            para_length = 500
            paragraphs = new_text.split("\n\n")
            for paragraph in paragraphs:
                if len(paragraph) > para_length:
                    one_line = re.sub("\n"," ", paragraph)
                    raw_text = raw_text + " " + one_line
            # block_length = 35  # minimum needed number of words in a paragraph
            # raw = parser.from_file(path, xmlContent=True)
            # xml = raw['content']
            # soup = BeautifulSoup(xml, features="html.parser")
            # for paragraph in soup.findAll('p'):
            #     text = paragraph.get_text()
            #     words = text.split(" ")
            #     if len(words) >= block_length:
            #         raw_text += text
            if len(raw_text) >= combine:
                tokens = np.stack(enc.encode(raw_text))
                token_chunks.append(tokens)
                raw_text = ''
            else:
                raw_text += '<|endoftext|>'

        elif path.endswith('.txt'):
            # Plain text
            with open(path, 'r', encoding="utf-8", errors="ignore") as fp:
                raw_text += fp.read()
            if len(raw_text) >= combine:
                tokens = np.stack(enc.encode(raw_text))
                token_chunks.append(tokens)
                raw_text = ''
            else:
                raw_text += '<|endoftext|>'
        else:
            print('File is not of type [.npz,.pdf,.txt]:', path)

    if raw_text:
        tokens = np.stack(enc.encode(raw_text))
        token_chunks.append(tokens)
    return token_chunks


def binary_search(f, lo, hi):
    if f(lo) or not f(hi):
        return None
    while hi > lo + 1:
        mid = (lo + hi) // 2
        if f(mid):
            hi = mid
        else:
            lo = mid
    return hi


class Sampler(object):
    """Fairly samples a slice from a set of variable sized chunks.

    'Fairly' means that the distribution is the same as sampling from one concatenated chunk,
    but without crossing chunk boundaries."""

    def __init__(self, chunks, seed=None):
        self.chunks = chunks
        self.total_size = sum(chunk.shape[0] for chunk in chunks)
        self.boundaries = [0]
        for i in range(len(chunks)):
            self.boundaries.append(self.boundaries[-1] + chunks[i].shape[0])
        self.rs = np.random.RandomState(seed=seed)

    def sample(self, length):
        assert length < self.total_size // len(
            self.chunks
        ), "Dataset files are too small to sample {} tokens at a time".format(
            length)
        while True:
            index = self.rs.randint(0, self.total_size - length - 1)
            i = binary_search(lambda j: self.boundaries[j] > index, 0,
                              len(self.boundaries) - 1) - 1
            if self.boundaries[i + 1] > index + length:
                within_chunk = index - self.boundaries[i]
                return self.chunks[i][within_chunk:within_chunk + length]
