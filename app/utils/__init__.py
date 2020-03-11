from functools import reduce
from itertools import chain

from nltk.corpus import reuters


def union_over_lists(lists):
    return reduce((lambda x, y: list(set(x) | set(y))), lists, [])


def intersection_over_lists(lists):
    return reduce((lambda x, y: list(set(x) & set(y))), lists)


def get_collection():
    collection = []
    for doc_id in reuters.fileids():
        collection.append(reuters.raw(doc_id))
    return collection


def get_levenshtein_distance(word1, word2):
    """
    :param word1:
    :param word2:
    :return:
    """
    word2 = word2.lower()
    word1 = word1.lower()
    matrix = [[0 for _ in range(len(word2) + 1)] for _ in range(len(word1) + 1)]

    for x in range(len(word1) + 1):
        matrix[x][0] = x
    for y in range(len(word2) + 1):
        matrix[0][y] = y

    for x in range(1, len(word1) + 1):
        for y in range(1, len(word2) + 1):
            if word1[x - 1] == word2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1
                )

    return matrix[len(word1)][len(word2)]


def rotate_word_around(symbol, word, remove_symbol=False):
    symbol_pos = symbol if isinstance(symbol, int) else word.find(symbol)
    if symbol_pos != -1:
        start = symbol_pos + 1 if remove_symbol else symbol_pos
        end = symbol_pos
        return word[start:] + word[:end]
    return word


def permute_word(word):
    permutations = []
    for i in range(len(word) - 1):
        permutations.append(rotate_word_around(i, word))
    return permutations


def permuterm(words):
    res = []
    for word in words:
        res += permute_word(word + '$')
    return res
