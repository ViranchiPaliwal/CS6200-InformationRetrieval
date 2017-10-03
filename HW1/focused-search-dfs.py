import urlparse
from bs4 import BeautifulSoup
from collections import deque
import sys
import os
import requests
import time

# Below are the constants which are being used throughout the program.
sys.setrecursionlimit(2000)
# the seed_page is a list that contains the seed_url and it's depth
seed_page = ['https://en.wikipedia.org/wiki/Sustainable_Energy', 1]
domain_name = 'https://en.wikipedia.org'
# the queue is the to do list that contains the links that need to be crawled
queue = deque([])
# the crawled list contains the list of links already crawled
crawled = []
count = 0
# the directory constant helps in making the directory to write the files'
directory = 'downloaded-content-focused-search-dfs'
max_depth = 5
queue_href = []
# the two keywords that need to be searched for in the links
keyword_1 = 'solar'
keyword_2 = 'Solar'


def main():
    print
    print "==================="
    print "Page to be crawled: " + seed_page[0]
    print "==================="
    print
    crawl(seed_page, count)
    # print_links_in_queue(queue)
    # this function prints out the crawled list in the directory
    print_links_in_crawled(crawled)


# The crawl() function performs the crawling using recursion.
def crawl(seed_page, count):
    # check if the link in question is present in the crawled list, if present then do not crawl it else go ahead with
    # crawling
    if seed_page[0] not in crawled:
        count += 1
        depth = seed_page[1]
        queue_reverse = deque([])

        # check condition to break the recursion
        if len(crawled) >= 1000 or depth > max_depth:
            return

        # appends the link in question to the crawled list, only adding the link and not the depth
        crawled.append(seed_page[0])

        # get the html file in text format
        html_text = requests.get(seed_page[0]).text.encode('ascii', 'replace')

        # assign a beautiful soup object to work on
        soup = BeautifulSoup(html_text, "html.parser")
        # this decomposes or drops the tables in the html cause we do not want to crawls links present in tables
        if '<table' in html_text:
            soup.table.decompose()

        # self created download function to download the url contents you could uncomment this if you want to download each file too
        # download_page(html_text, seed_page[0])

        print str(count) + ')' + ' at DEPTH: ' + str(seed_page[1]) + ',' + ' Now crawling: ' + seed_page[0]

        # find all 'a' tags in the page
        hrefs = soup.findAll('a', href=True)
        for tags in hrefs:
            tags['href'] = urlparse.urljoin(domain_name, tags['href'])
            link = [tags['href'], depth]
            anchor_text = tags.text

            # calling the valid function that checks if the link is valid  and then only adds it to the queue.
            # and when depth is less than max depth
            if valid(domain_name, tags['href'], anchor_text) and depth + 1 < max_depth:
                queue_reverse.appendleft(link)
                queue_href.append(tags['href'])

        for i in queue_reverse:
            queue.append(i)
    # the reverse queue is used cause in traditional stack popping the dfs will become post ordered but we need to
    # crawl the link which is coming first on the page preorder (i.e. the leftmost link). Hence I take in the links
    # in a reversed order and then pop the rightmost link of the queue giving me the first link of that depth.
    # Thus implementing DFS preordered.

    # if length of queue is more then zero then only pop
    if len(queue) > 0:
        # popping the right most element in the queue and adding it to the current which is a temp variable
        current = queue.pop()
        current_page = (current[0], current[1] + 1)
        time.sleep(1)
        crawl(current_page, count)
    else:
        return


# the valid function checks if the link in question meet the following criteria
def valid(domain_name, link, anchor_text):
    if domain_name in link and link not in crawled and '#' not in link and ':' not in link[6:] \
            and extension_check(link) and '?' not in link and 'Main_Page' not in link \
            and '/' not in link[31:] and (keyword_1 in link or keyword_2 in link or keyword_1 in anchor_text or keyword_2 in anchor_text):
        return True
    else:
        return False


# def print_links_in_queue(queue):
#    for i in queue:
#        with open(directory + '/' + 'queue.txt', 'a') as f:
#            f.write(i[0] + '\n')


def print_links_in_crawled(crawled):
    for i in crawled:
        with open('crawled-task2-dfs.txt', 'a') as f:
            f.write(i + '\n')


# Check if the following extension are not present in the link. If present then we need to not add the link to the queue
def extension_check(link):
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.tif', '.txt']
    i = 0
    flag = True
    while i < (len(extensions)):
        if extensions[i] in link:
            flag = False
        else:
            i += 1
    return flag


# this function creates a new directory if not already present and then adds the downloaded files one by one
def download_page(html_text, page):
    this_page = page[30:]
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)
    with open(directory + '/' + this_page + '.txt', 'w+') as f:
        f.write(html_text)


main()