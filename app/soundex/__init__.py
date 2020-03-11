import json


def soundex(query: str):
    """
    :param query:
    :return:
    """

    # Step 0: Clean up the query string
    query = query.lower()
    letters = [char for char in query if char.isalpha()]

    # Step 1: Save the first letter. Remove all occurrences of a, e, i, o, u, y, h, w.

    # If query contains only 1 letter, return query+"000" (Refer step 5)
    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    # Step 2: Replace all consonants (include the first letter) with digits according to rules

    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    # Step 3: Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    # Step 4: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    # Step 5: Append 3 zeros if result contains less than 3 digits.
    # Remove all except first letter and 3 digits after it.

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(letter) for letter in letters])

    return string


def build_soundex_index(index):
    """
    Construct soundex index from inverted index.
    """

    print('\n\n\n Building SOUNDEX -\n\n\n')

    soundex_index = {}
    for word in index:
        word_soundex = soundex(word)
        if word_soundex in soundex_index:
            soundex_index[word_soundex].append(word)
        else:
            soundex_index[word_soundex] = [word]

    print('\n\n\n SOUNDEX built \n\n\n')
    return soundex_index


def add_to_soundex(soundex_index, word):
    word_soundex = soundex(word)
    if word_soundex in soundex_index:
        soundex_index[word_soundex].append(word)
    else:
        soundex_index[word_soundex] = [word]


def save_soundex_to_redis(redis_db, soundex_index):
    redis_db.set('soundex', json.dumps(soundex_index))


def get_soundex_from_redis(redis_db):
    return json.loads(redis_db.get('soundex'))
