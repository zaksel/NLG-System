import difflib
#import Levenshtein
import distance
from sklearn.feature_extraction.text import TfidfVectorizer

output = "Push the button at right to activate the camera and take pictures of your family and the animals."
target = "Push the button on the right to activate the camera and take pictures of your family or animals."


#https://stackoverflow.com/questions/6690739/high-performance-fuzzy-string-comparison-in-python-use-levenshtein-or-difflib
diffl = difflib.SequenceMatcher(None, output, target).ratio()
#lev = Levenshtein.ratio(output, target)
jac = 1 - distance.jaccard(output, target)
print(diffl, jac)

corpus = []
corpus.append(output)
corpus.append(target)
vect = TfidfVectorizer(min_df=1, stop_words="english")
tfidf = vect.fit_transform(corpus)
pairwise_similarity = tfidf * tfidf.T

print(pairwise_similarity.toarray())

