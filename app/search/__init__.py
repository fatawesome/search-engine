from app.documents import get_from_collection
from app.inverted_index import get_from_index
from app.soundex import soundex
from app.utils import union_over_lists, get_levenshtein_distance, rotate_word_around, intersection_over_lists
from app.utils.preprocess import preprocess_pipeline, tokens_logical_parser


def perform_search(db, query, prefix_tree, soundex_index):
    """
    Perform search on given query.
    """

    query_tokens = preprocess_pipeline(query)
    logical_tokens = tokens_logical_parser(query_tokens)
    results_per_token = [
        get_docs_per_token(
            db=db,
            token=token,
            operator=operation,
            prefix_tree=prefix_tree,
            soundex_index=soundex_index
        )
        for token, operation in logical_tokens
    ]

    result_ids = intersection_over_lists([x for x in results_per_token])

    relevant = [get_from_collection(db, idx) for idx in result_ids]

    return relevant


def wildcard_search(db, term, prefix_tree):
    """
    Perform search on wildcard query
    in the given prefix tree and inverted index.
    """

    permuted_term = rotate_word_around('*', (term + '$'), True)
    matches = prefix_tree.has_prefix(permuted_term)

    words = [rotate_word_around('$', word, True) for word in matches]

    index_results = []

    for word in words:
        preprocessed_word = preprocess_pipeline(word)[0]

        docs_by_word = get_from_index(db, preprocessed_word)

        if docs_by_word:
            index_results.append(docs_by_word['doc_ids'])

    return union_over_lists(index_results)


def get_docs_per_token(db, token, operator, prefix_tree, soundex_index):
    """
    Perform search for each token individually.
    """

    found = []

    if operator == '|':
        found = wildcard_search(
            db=db,
            term=token,
            prefix_tree=prefix_tree
        )
    else:
        res_from_index = get_from_index(db, token)

        if res_from_index:
            found = res_from_index['doc_ids']
        else:
            soundex_token = soundex(token)
            if soundex_token in soundex_index:
                soundex_results = soundex_index[soundex_token]
                levenstein_results = \
                    [word for word in soundex_results if get_levenshtein_distance(token, word) < 3]
                lists = [get_from_index(db, word)['doc_ids'] for word in levenstein_results]
                found = union_over_lists(lists)

    return found
