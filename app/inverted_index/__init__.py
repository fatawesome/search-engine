from app.utils.preprocess import preprocess_pipeline

# # # # # # #
# WORK WITH DATABASE
# # # # # # #


def get_index_from_db(db):
    return db.inverted_index.find()


def get_from_index(db, word):
    return db.inverted_index.find_one({
        'word': word
    })


def set_in_index(db, word, doc_ids):
    db.inverted_index.insert_one({
        'word': word,
        'doc_ids': doc_ids
    })


def add_doc_to_index(db, word, doc_id):
    if get_from_index(db, word):
        db.inverted_index.update_one(
            {'word': word},
            {'$push': {'doc_ids': doc_id}}
        )
    else:
        set_in_index(db, word, [doc_id])


def delete_doc_from_index(db, doc_id):
    db.inverted_index.update_many(
        {},
        {'$pull': {'doc_ids': doc_id}}
    )


def save_inverted_index_to_db(db, index):
    for word, doc_ids in index.items():
        set_in_index(db, word, doc_ids)


# # # # # # #
# HELPERS
# # # # # # #

def build_inverted_index_from_collection(collection):
    """
    Construct inverted index from collection of documents.
    """

    inverted_index = {}
    for idx, doc in enumerate(collection):
        text = preprocess_pipeline(doc)
        for word in text:
            if word in inverted_index:
                if idx not in inverted_index[word]:
                    inverted_index[word].append(idx)
            else:
                inverted_index[word] = [idx]
    return inverted_index
