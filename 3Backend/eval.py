import difflib
#import Levenshtein
import distance
from sklearn.feature_extraction.text import TfidfVectorizer

import sys
sys.setrecursionlimit(1500)

output = "If the viewfinder can make you go faster or if not sharp and the resolution is fast then double check out this video showing how to use eyepiece diopter adjustment on a high end lens and a knob with a built in diopter near to the eyepiece. I've already mentioned the On-Off control option can be used on a small button for a zoom lens a handgrip on the right side of the control panel with thumb thumb is to turn the zoom lens in one press, press the one you want the recording will be started the next time a second lens is turned on then press the stop."
target = "If the viewfinder image is still not sharp, you should now check that the eyepiece diopter adjustment is correct for your eyesight: you will find the adjustment ring or knob for this near to the eyepiece. On-off control of the camcorder is simplicity itself. You will find the camera button located close to the hand-grip on the right hand side of the body. Usually, it is positioned so that it can be operated by the thumb, and normally one press is needed to start recording and a second press to stop."

memo = {}
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    cost = 0 if s[-1] == t[-1] else 1

    i1 = (s[:-1], t)
    if not i1 in memo:
        memo[i1] = levenshtein(*i1)
    i2 = (s, t[:-1])
    if not i2 in memo:
        memo[i2] = levenshtein(*i2)
    i3 = (s[:-1], t[:-1])
    if not i3 in memo:
        memo[i3] = levenshtein(*i3)
    res = min([memo[i1] + 1, memo[i2] + 1, memo[i3] + cost])
    return res

#https://stackoverflow.com/questions/6690739/high-performance-fuzzy-string-comparison-in-python-use-levenshtein-or-difflib
diffl = difflib.SequenceMatcher(None, output, target).ratio()
lev = levenshtein(output, target)
lev_rel = (max(len(output),len(target))-lev)/(max(len(output),len(target)))
jac = 1 - distance.jaccard(output, target)
print(lev_rel)
print(jac)

corpus = []
corpus.append(output)
corpus.append(target)
vect = TfidfVectorizer(min_df=1, stop_words="english")
tfidf = vect.fit_transform(corpus)
pairwise_similarity = tfidf * tfidf.T

print(pairwise_similarity.toarray())

