from datetime import datetime
import math

# Compute the PageRank of every page in the data.
# List the top 50 pages by the PageRank score


def main():
    start = datetime.now()
    inlink_file = "g1graph.txt"
    d = 0.85
    inlinks_dict = {}
    outlinks_dict = {}
    set_of_pages = set()
    in_file = open(inlink_file, 'r')
    pagerank = {}
    set_of_sinks = []
    no_of_iteration = 0
    updated_pagerank = {}
    count = 0

    # read the data from the file and create a link graph of the given data
    for pages in in_file.readlines():
        page = pages.split()[0]
        set_of_pages.add(page)

        inlinks = set(pages.split()[1:])
        inlinks_dict[page] = inlinks

        for inlink in inlinks:
            if inlink in outlinks_dict:
                outlinks_dict[inlink].append(page)
            else:
                outlinks_dict[inlink] = [page]
            outlinks_dict[inlink] = list(set(outlinks_dict[inlink]))

    # create a set of all the pages that are not present in the outlinks
    for link in inlinks_dict.keys():
        if link not in outlinks_dict:
            set_of_sinks.append(link)

    number_of_pages = len(set_of_pages)

    # assign initial pageRank to all the pages
    for link in set_of_pages:
        pagerank[link] = 1.0/float(number_of_pages)

    # assigning initial perplexity
    previous_perplexity = calculate_perplexity(pagerank)

    while 1:
        count += 1
        print "count in while::", count
        sinkPR = 0.0

        for page in set_of_sinks:
            sinkPR += float(pagerank[page])

        for page in set_of_pages:
            # teleportation factor
            updated_pagerank[page] = (1.0 - d) / float(number_of_pages)
            # spread remaining sink PR evenly
            updated_pagerank[page] += (d * sinkPR/float(number_of_pages))

            for link in inlinks_dict[page]:
                temp = outlinks_dict[link]
                # add share of PageRank from in-links
                updated_pagerank[page] += (d * pagerank[link])/float(len(temp))
            pagerank[page] = updated_pagerank[page]

        current_perplexity = calculate_perplexity(pagerank)

        # write perplexity values of each iteration to a file
        perplexity_file = open('perplexity.txt', 'a')
        perplexity_file.write('Iteration ' + str(count) + ': ' + str(current_perplexity) + '\n')
        perplexity_file.close()

        # difference between old and new value will determine convergence
        if find_difference(previous_perplexity, current_perplexity) < 1 and no_of_iteration < 4:
            no_of_iteration += 1

        elif find_difference(previous_perplexity, current_perplexity) > 1:
            no_of_iteration = 0

        else:
            break
        # get a new value of perplexity based on the updated link pages
        previous_perplexity = current_perplexity

    print "iterations:", no_of_iteration

    output_pagerank_file = "pageRank.txt"
    sorted_pagerank = sorted(pagerank.items(), key=lambda (x): x[1], reverse=True)[:50]
    print_file = open(output_pagerank_file, 'w')

    count = 0

    # output to a file
    for page in sorted_pagerank:
        count += 1
        print_file.write(str(count) + "\t" + page[0] + ": " + str(page[1]) + "\n")

    print_file.close()

    print "sum:", sum(pagerank.values())

    total_time = datetime.now() - start
    print total_time


def calculate_entropy(pagerank_dict):
    entropy_value = 0
    for page in pagerank_dict.keys():
        p = pagerank_dict[page]
        value1 = math.log((float(1)/float(p)), 2)
        temp_value = float(p * value1)
        entropy_value += temp_value
    return entropy_value


def calculate_perplexity(pagerank_dict):
    entropy_value = calculate_entropy(pagerank_dict)
    perplexity_val = math.pow(2, entropy_value)
    return perplexity_val


def find_difference(val1, val2):
    diff = val1 - val2
    return math.fabs(diff)

main()







