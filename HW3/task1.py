from bs4 import BeautifulSoup
import os
import glob
import re
import traceback

# all_files maintains the list of all the file names
all_files = []
directory = 'corpus'


# fetches the raw wikipedia articles that was downloaded in HW1 and tokenizes them
def get_content():
    try:
        count = 1
        path = 'downloaded_content'
        for filename in glob.glob(os.path.join(path, '*.txt')):
            with file(filename) as f:
                url = f.readline()
                article_name = (url.split("https://en.wikipedia.org/wiki/"))[-1][:-1]
                article_name = article_name.replace('_', '').replace('-', '').replace('/', '').\
                    replace('%', '').replace('(','').replace(')', '')
                print str(count) + ') ' + 'Generating corpus of: ' + article_name
                content = f.read()
                content = content.lower()
                count += 1

                soup = BeautifulSoup(content, 'html.parser')
                soup.prettify().encode('utf-8')

                title_text = soup.find('title').get_text().encode('utf-8')
                header_text = soup.find('h1').get_text().encode('utf-8')
                data = soup.findAll('div', attrs={'id': 'bodycontent'})
                body_text = ''
                for div in data:
                    body_text += div.get_text().encode('utf-8')
                content_text = title_text + header_text + body_text
                processed_text = text_transformation(content_text)
                write_to_file(processed_text, article_name)
                f.close()
    except:
        print 'Error in try block of fetch_content!'
        print traceback.format_exc()


# perform text transformation on the string provided to it as argument
def text_transformation(content):
    content = re.sub(r'[@_!\s^&*?#=+$~%:;\\/|<>(){}[\]"\']', ' ', content)
    content_word_list = []
    for word in content.split():
        word_length = len(word)
        if word[word_length - 1:word_length] == '-' or word[word_length - 1:word_length] == ',' or word[word_length - 1:word_length] == '.':
            word = word[:word_length - 1]
            content_word_list.append(remove_punctuation(word))
        else:
            content_word_list.append(remove_punctuation(word))
    content_word_list = [x for x in content_word_list if x != '']
    content_word_list = " ".join(content_word_list)
    return content_word_list


# removes irrelevant punctuations before a word
def remove_punctuation(word):
    while word[:1] == "-" or word[:1] == "," or word[:1] == ".":
        if re.match(r'^[\-]?[0-9]*\.?[0-9]+$', word):
            return word
        if word[:1] == "-" or word[:1] == "." or word[:1] == ",":
            word = word[1:]
        else:
            return word
    return word


# writes the contents in file
def write_to_file(content, file_name):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_index_terms = open(directory + '/' + file_name + '.txt', 'w')
        file_index_terms.write(content)
        file_index_terms.close()
    except:
        print "Error in try block of write_to_file!"
        print traceback.format_exc()


def main():
    get_content()

main()
