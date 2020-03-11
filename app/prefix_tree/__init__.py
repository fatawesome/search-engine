import pickle

from app.utils import permuterm
from app.utils.preprocess import remove_stop_word, tokenize, normalize
import json


class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()

    def add_child(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key

    def __str__(self):
        return self.label

    def __getitem__(self, key):
        return self.children[key]


class Trie:
    """
    Prefix tree (Trie) implementation
    is inspired by this code: https://gist.github.com/nickstanisha/733c134a0171a00f66d4
    """

    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, word):
        current_node = self.head
        word_finished = True

        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break

        if not word_finished:
            while i < len(word):
                current_node.add_child(word[i])
                current_node = current_node.children[word[i]]
                i += 1

        current_node.data = word

    def has_word(self, word):
        if not isinstance(word, str):
            raise ValueError('Trie.has_word() needs a string.')
        if len(word) == 0:
            return False

        current_node = self.head
        exists = True

        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        if exists:
            if current_node.data == None:
                exists = False

    def has_prefix(self, prefix):
        """List of words with given prefix (if present)"""
        words = []
        if prefix == None:
            raise ValueError('Trie.has_prefix() needs a string.')

        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                return words

        if top_node == self.head:
            queue = [node for key, node in top_node.children.iteritems()]
        else:
            queue = [top_node]

        while queue:
            current_node = queue.pop()
            if current_node.data != None:
                words.append(current_node.data)

            queue = [node for key, node in current_node.children.items()] + queue

        return words

    def get_data(self, word):
        if not self.has_word(word):
            raise ValueError(f'{word} not found in trie')

        current_node = self.head
        for letter in word:
            current_node = current_node[letter]

        return current_node.data


def preprocess_for_trie(text):
    """
    Preprocess text before building prefix tree.
    Doesn't contain lemmatization.
    """

    return remove_stop_word(tokenize(normalize(text)))


def prepare_collection(collection):
    """
    Transform collection of documents
    to list of words.
    """

    words = []
    for doc in collection:
        text = preprocess_for_trie(doc)
        for word in text:
            words.append(word)
    return words


def build_prefix_tree(collection):
    """
    Construct prefix tree from collection of documents.
    """
    words = prepare_collection(collection)

    permutermed_words = permuterm(words)
    trie = Trie()
    for word in permutermed_words:
        trie.add(word)

    return trie


def add_to_prefix_tree(prefix_tree, text):
    words = [word for word in preprocess_for_trie(text)]
    permuted_words = permuterm(words)

    for word in permuted_words:
        prefix_tree.add(word)


def save_prefix_tree_to_redis(redis_db, prefix_tree):
    redis_db.set('prefix_tree', pickle.dumps(prefix_tree))


def get_prefix_tree_from_redis(redis_db):
    res = pickle.loads(redis_db.get('prefix_tree'))
    return res
