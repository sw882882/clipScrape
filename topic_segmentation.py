import nltk
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.stem import WordNetLemmatizer
from clean import *

# download required NLTK packages
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# load the document
text = diarized_srt_to_sentence_srt("./source/trashtastestourists.wav.word.srt")

print(text)

# preprocess the document using NLTK's default tokenizer and stopword list
words = nltk.tokenize.word_tokenize(text)
words = [
    word.lower()
    for word in words
    if word.isalpha() and word.lower() not in nltk.corpus.stopwords.words("english")
]

# lemmatize the words
lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

# join the words back into a string
processed_text = " ".join(lemmatized_words)

# create a TextTilingTokenizer object
tt = TextTilingTokenizer(k=2, w=5)

# apply TextTiling to the preprocessed document
tilings = tt.tokenize(processed_text)

# print the tile boundaries
for i, boundary in enumerate(tilings[1:]):
    print(f"Tile {i+1} boundary: {boundary:.2f}")
