# # # # # # #
# WORK WITH DATABASE
# # # # # # #


def get_collection_from_db(db):
    return list(db.documents.find())


def get_from_collection(db, id):
    return db.documents.find_one({
        'id': id
    })


def set_in_collection(db, id, doc):
    db.documents.insert_one({
        'id': id,
        'doc': doc
    })


def delete_from_collection(db, id):
    db.documents.delete_one({'id': id})


def save_collection_to_db(db, collection):
    for idx, doc in enumerate(collection):
        set_in_collection(db, idx, doc)

