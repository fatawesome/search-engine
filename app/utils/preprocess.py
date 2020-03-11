import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def normalize(text):
    """
    Normilize given text
    """

    alphabetical_regex = re.compile('[^a-zA-Z |*]')
    res = alphabetical_regex.sub('', text.lower())
    return res


def tokenize(text):
    """
    Tokenize text using nltk lib
    """

    return nltk.word_tokenize(text)


def lemmatization(tokens):
    """
    Lemmatize given tokens
    """

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def remove_stop_word(tokens):
    """
    Remove stop-words (as, if, a, the, etc.)
    from given tokens.
    """

    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]


def preprocess_pipeline(text):
    """
    Preprocess given text
    for inverted index creation.
    """

    return remove_stop_word(lemmatization(tokenize(normalize(text))))


def tokens_logical_parser(tokens):
    """
    Parse tokens to determine logical operation.
    """

    return [(token, '|' if token.find('*') != -1 else '&') for token in tokens]
