import math
import sqlite3
import argparse

from pprint import pprint

from nltk.corpus import stopwords
from helpers import is_path_correct

cws = ['μας.', 'σας', 'τη', 'μας', 'Η', 'σας.', 'της', 'Το', 'Για', 'This', 'Ο', '.', 'σου', 'ότι', 'αυτό.', 'είστε', 'Τα', 'μας,', 'από']

def calculate_tf(words, doc_len):
    tf = {}
    for word, count in words.items():
        tf[word] = count / float(doc_len)
    return tf

def calculate_idf(docs):
    N = len(docs)
    idf = dict.fromkeys(docs[0].keys(), 0)
    for doc in docs:
        for word, val in doc.items():
            if val > 0:
                idf[word] += 1
    
    for word, count in idf.items():
        if count > 0:
            idf[word] = math.log(N / float(count))

    return idf

def calculate_tf_idf(words, idfs):
    tf_idf = {}
    for word, val in words.items():
        tf_idf[word] = val * idfs[word]
    return tf_idf

def calculate_word_frequency(rows):
    unique_words = set()
    privacy_texts = list()

    common_words = set(stopwords.words('english'))
    common_words.update(set(stopwords.words('greek')))
    common_words.update(set(cws))

    for row in rows:
        privacy_text = row[0]
        privacy_text_arr = set(privacy_text.split(' ')).difference(common_words)

        unique_words = unique_words.union(privacy_text_arr)

        privacy_texts.append(privacy_text_arr)

    tfs = list()
    docs = list()

    for privacy_text_arr in privacy_texts:
        document = dict.fromkeys(unique_words, 0)
        for word in privacy_text_arr:
            if len(word) == 0: #empty entries
                continue
            document[word] += 1
        
        tf = calculate_tf(document, len(privacy_text_arr))

        tfs.append(tf)
        docs.append(document)

    idfs = calculate_idf(docs)
    tf_idfs = list()

    for tf in tfs:
        tf_idf = calculate_tf_idf(tf, idfs)
        tf_idfs.append(tf_idf)

    word_frequencies = dict.fromkeys(unique_words, 0)
    for tf_id in tf_idfs:
        for k, v in tf_id.items():
            if k == '':
                continue
            word_frequencies[k] += v

    for word, frequency in word_frequencies.items():
        word_frequencies[word] = frequency / len(tf_idfs)

    res = list(sorted(word_frequencies.items(), key=lambda item: item[1]))
    return res[-50:]

def calculate_avg_word_count(rows):
    total_rows = len(rows)
    total_words = 0

    for row in rows:
        privacy_text = row[0]
        total_words += len(privacy_text.split(' '))
    return total_words / total_rows

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='./outp/cookies.sqlite', type=is_path_correct)
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    cur.execute("SELECT privacy_text FROM cookie_options")
    rows = cur.fetchall()
    conn.close()

    print('Total cookie banners: {}'.format(len(rows)))
    print('Average word count: {}'.format(calculate_avg_word_count(rows)))
    print()

    print('Average term frequency')
    term_frequencies = calculate_word_frequency(rows)
    for term_frequency in term_frequencies:
        print('{}\t{}'.format(term_frequency[0], term_frequency[1]))
