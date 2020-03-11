import json

from flask import request

from . import application, db, redis_db
from .documents import save_collection_to_db, get_collection_from_db, set_in_collection, delete_from_collection
from .inverted_index import build_inverted_index_from_collection, save_inverted_index_to_db, \
    add_doc_to_index, delete_doc_from_index
from .prefix_tree import build_prefix_tree, save_prefix_tree_to_redis, get_prefix_tree_from_redis, add_to_prefix_tree
from .search import perform_search
from .soundex import build_soundex_index, save_soundex_to_redis, get_soundex_from_redis, add_to_soundex
from .utils import get_collection
from .utils.preprocess import preprocess_pipeline


@application.route('/')
def index():
    return "Hello worldddd"


@application.route('/create-reuters-index')
def create_first_reuters_index():
    reuters_collection = get_collection()
    reuters_collection = reuters_collection[:len(reuters_collection) - 5]
    print('--- got collection', flush=True)
    print(reuters_collection[0], flush=True)

    save_collection_to_db(db, reuters_collection)
    print('--- saved collection', flush=True)

    inverted_index = build_inverted_index_from_collection(reuters_collection)
    print('--- built inverted index', flush=True)

    save_inverted_index_to_db(db, inverted_index)
    print('--- saved inverted index', flush=True)

    soundex = build_soundex_index(inverted_index)
    print('--- built soundex index', flush=True)

    save_soundex_to_redis(redis_db, soundex)
    print('--- saved soundex', flush=True)

    db_collection = get_collection_from_db(db)
    print('--- got collection from db', db_collection[0])

    prefix_tree = build_prefix_tree(reuters_collection)
    print(len(prefix_tree['t'].children), flush=True)
    print('--- built prefix tree', flush=True)

    save_prefix_tree_to_redis(redis_db, prefix_tree)
    print('--- saved prefix tree', flush=True)

    return "лул."


@application.route('/search')
def search():
    query = request.args.get('q')

    res = perform_search(
        db,
        query,
        get_prefix_tree_from_redis(redis_db),
        get_soundex_from_redis(redis_db)
    )

    print(res, flush=True)
    if len(res) > 0:
        res = [{'id': x['id'], 'doc': x['doc']} for x in res if x]

    return json.dumps(res)


@application.route('/add-second-half')
def add_second_half_reuters_index():
    reuters_collection = get_collection()
    reuters_collection = reuters_collection[len(reuters_collection) - 4:]

    current_id = list(db.documents.find().sort([('id', -1)]).limit(1))[0]['id']

    soundex_index = get_soundex_from_redis(redis_db)
    prefix_tree = get_prefix_tree_from_redis(redis_db)

    for doc in reuters_collection:
        current_id += 1
        set_in_collection(db, current_id, doc)

        print('-----', flush=True)
        print(current_id, flush=True)
        print('-----', flush=True)

        text = preprocess_pipeline(doc)
        for word in text:
            add_doc_to_index(db, word, current_id)
            add_to_soundex(soundex_index, word)

        add_to_prefix_tree(prefix_tree, doc)

    save_prefix_tree_to_redis(redis_db, prefix_tree)
    save_soundex_to_redis(redis_db, soundex_index)

    return "mem."


@application.route('/delete-doc')
def delete_document():
    id = int(request.args.get('id'))
    print('-----', flush=True)
    print(id, flush=True)
    print('-----', flush=True)

    # delete_doc_from_index(db, id)
    # delete_from_collection(db, id)
    db.documents.delete_one({'id': id})

    print('-----', flush=True)
    print(db.documents.find({'id': id}), flush=True)
    print('-----', flush=True)
    return 'ydolil.'
