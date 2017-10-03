import glob
import os
import traceback
import math

# dictionary of the documents and their corresponding term frequency
token_count = {}
# dictionary of the document names and their corresponding document IDs
document_name_dict = {}
# total number of documents
no_of_docs = 989


# creates an inverted index for the unigram
def inverted_index_unigram():
    inverted_index = {}
    doc_id = 0
    try:
        # reads each file from corpus
        for filename in glob.glob(os.path.join('corpus', '*.txt')):
            with file(filename) as f:
                doc_id += 1
                doc = f.read()
                file_key = str(filename).split('corpus/')[1][:-4]
                print "Generating index for " + file_key
                token_count[file_key] = len(doc.split())
                document_name_dict.update({file_key: doc_id})
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


# computes the BM25 score for the given query
def bm25(query_string, inverted_index):
    score_dict = {}
    term_dict = {}
    # calculating the variables that remain constant for the query 
    k1 = 1.2
    k2 = 100
    b = 0.75
    avdl = sum(token_count.values()) / float(no_of_docs)
    term_list = query_string.split(' ')
    # create a term_dict to keep track of unique terms in the query 
    # which will be helpful later to calculate the qf
    for term in term_list:
        if term in term_dict:
            term_dict[term] += 1
        else:
            term_dict[term] = 1
    # for each document in token_count
    for doc in token_count:
        dl = token_count[doc]
        K = k1 * ((1 - b) + (b * (dl / avdl)))
        score = 0
        # for each term in term_dict
        for term in term_dict:
            qf = term_dict[term]
            n = len(inverted_index[term])
            doc_dict = inverted_index[term]
            if doc in doc_dict:
                f = doc_dict[doc]
            else:
                f = 0
            temp1 = math.log10((no_of_docs - n + 0.5)/(n + 0.5))
            temp2 = (((k1 + 1) * f) / (K + f))
            temp3 = (((k2 + 1) * qf) / (k2 + qf))
            # calculate the score and append it to the itself for the next term
            score += temp1 * temp2 * temp3
        score_dict[doc] = score
    sorted_doc_scores = sorted(score_dict.items(), key=lambda (x): x[1], reverse=True)
    return sorted_doc_scores


# prints the ranked list into a file in the specified format
def print_ranked_list(inverted_index):
    file_query = open('query_file.txt', 'r')

    for line in file_query.readlines():
        query_list = line.split(' ')
        query_id = query_list[0]
        query_string = ' '.join(query_list[1:])[:-1].lower()
        print 'The query is: ' + query_string
        print 'Generating ranked list....'
        sorted_ranked_docs = bm25(query_string, inverted_index)

        if len(sorted_ranked_docs) == 0:
            print 'No matching documents found!'
        else:
            print 'Printing ranked list....'
            doc_file = open('Ranked_doc_list_BM25.txt', 'a')
            for count in range(min(len(sorted_ranked_docs), 100)):
                rank = count + 1
                doc_file.write(str(query_id) + ' Q0 ' + str(sorted_ranked_docs[count][0]) + ' ' + str(rank) + ' '
                           + str(sorted_ranked_docs[count][1]) + ' BM25' + '\n')
            doc_file.close()


def main():
    print 'Generating Inverted Index....'
    inverted_index = inverted_index_unigram()
    print_ranked_list(inverted_index)

main()