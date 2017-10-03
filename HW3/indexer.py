import glob
import os
import traceback


# creates an inverted index for unigram
def inverted_index_unigram():
    token_count = {}
    inverted_index = {}
    try:
        # reads each file from corpus
        for filename in glob.glob(os.path.join('corpus', '*.txt')):
            with file(filename) as f:
                doc = f.read()
                file_key = str(filename).split('corpus/')[1][:-4]
                print "Generating index for " + file_key
                token_count[file_key] = len(doc.split())
                # creates a dict inside a dict structure for the inverted index
                for word in doc.split():
                    if not inverted_index.has_key(word):
                        doc_dict = {file_key: 1}
                        inverted_index[word] = doc_dict
                    elif inverted_index[word].has_key(file_key):
                        doc_dict = inverted_index[word]
                        value = doc_dict.get(file_key)
                        value += 1
                        doc_dict[file_key] = value
                    else:
                        doc_dict = {file_key: 1}
                        inverted_index[word].update(doc_dict)
            f.close()
    except:
        print "Error in try block of inverted_index_unigram!"
        print traceback.format_exc()

    return inverted_index


# creates an inverted index for bigram
def inverted_index_bigram():
    token_count = {}
    inverted_index = {}
    try:
        # reads each file from corpus
        for filename in glob.glob(os.path.join('corpus', '*.txt')):
            with file(filename) as f:
                doc = f.read()
                file_key = str(filename).split('corpus/')[1][:-4]
                print 'Generating index for ' + file_key
                word_list = doc.split()
                token_count[file_key] = len(doc.split()) - 1
                # creates a dict inside a dict structure for the inverted index
                # considers each bigram as a word and the word to it's immidiate left
                for i in range(len(word_list) - 1):
                    word = word_list[i] + ' ' + word_list[i + 1]
                    if not inverted_index.has_key(word):
                        doc_dict = {file_key: 1}
                        inverted_index[word] = doc_dict
                    elif inverted_index[word].has_key(file_key):
                        doc_dict = inverted_index[word]
                        value = doc_dict.get(file_key)
                        value += 1
                        doc_dict[file_key] = value
                    else:
                        doc_dict = {file_key: 1}
                        inverted_index[word].update(doc_dict)
            f.close()
    except:
        print "Error in try block of inverted_index_bigram!"
        print traceback.format_exc()

    return inverted_index


# creates an inverted index for a trigram
def inverted_index_trigram():
    token_count = {}
    inverted_index = {}
    try:
        # reads each file from corpus
        for filename in glob.glob(os.path.join('corpus', '*.txt')):
            with file(filename) as f:
                doc = f.read()
                file_key = str(filename).split('corpus/')[1][:-4]
                print 'Generating index for ' + file_key
                word_list = doc.split()
                token_count[file_key] = len(doc.split()) - 2
                # creates a dict inside a dict structure for the inverted index
                # considers each trigram as 3 words in sequence to its left
                for i in range(len(word_list) - 2):
                    word = word_list[i] + ' ' + word_list[i + 1] + ' ' + word_list[i + 2]
                    if not inverted_index.has_key(word):
                        doc_dict = {file_key: 1}
                        inverted_index[word] = doc_dict
                    elif inverted_index[word].has_key(file_key):
                        doc_dict = inverted_index[word]
                        value = doc_dict.get(file_key)
                        value += 1
                        doc_dict[file_key] = value
                    else:
                        doc_dict = {file_key: 1}
                        inverted_index[word].update(doc_dict)
            f.close()
    except:
        print "Error in try block of inverted_index_trigram!"
        print traceback.format_exc()

    return inverted_index


def generate_term_freq_table(inverted_index, ngram):
    term_freq = {}

    for key in inverted_index:
        freq = 0
        doc_dict = inverted_index[key]
        for key2 in doc_dict:
            freq += doc_dict.get(key2)
        term_freq[key] = freq
    # sorts the table with the highest freq term at the top
    sorted_table = sorted(term_freq.items(), key=lambda (x): x[1], reverse=True)
    write_term_freq(sorted_table, ngram)


def write_term_freq(sorted_table, ngram):
    file_name = "term_freq_table" + "_" + str(ngram) + ".txt"
    f = open(file_name, 'w')
    for data in sorted_table:
        f.write(str(data[0]) + " " + str(data[1]) + "\n")
    f.close()


def generate_doc_freq_table(inverted_index, ngram):
    doc_freq = {}

    for key in inverted_index:
        doc_list = []
        doc_dict = inverted_index[key]
        for key2 in doc_dict:
            doc_list.append(key2)
        doc_freq[key] = doc_list
    # sorts the table in lexicographical order
    sorted_table = sorted(doc_freq.items(), key=lambda (x): x[0])
    write_doc_freq(sorted_table, ngram)


def write_doc_freq(sorted_table, ngram):
    file_name = 'doc_freq_table' + '_' + str(ngram) + '.txt'
    f = open(file_name, 'w')
    for data in sorted_table:
        f.write(str(data[0]) + ' ' + str(data[1]) + ' ' + str(len(data[1])) + '\n')
    f.close()


def main():
    n = raw_input('Enter the value of n for n-grams: ')
    if int(n) == 1:
        unigram = inverted_index_unigram()
        generate_term_freq_table(unigram, 'unigram')
        generate_doc_freq_table(unigram, 'unigram')

    elif int(n) == 2:
        bigram = inverted_index_bigram()
        generate_term_freq_table(bigram, 'bigram')
        generate_doc_freq_table(bigram, 'bigram')

    elif int(n) == 3:
        trigram = inverted_index_trigram()
        generate_term_freq_table(trigram, 'trigram')
        generate_doc_freq_table(trigram, 'trigram')

    else:
        print 'Enter either 1, 2 or 3'

main()