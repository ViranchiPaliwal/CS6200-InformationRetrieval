Assignment 2:
Goal: Link Analysis and PageRank Implementation

Summary:
This readme file has references and detailed information regarding how to setup, compile and run the programs in the assignment.
The tasks are discussed below in brief:
-- Task1: Obtaining directed web graphs
		A. Building our own: Build a graph for the 1000 URLs that we have crawled in HW1-Task1 by following their links and their corresponding in-link relationship. This graph is in the file 'g1graph.txt'
	    B. Using existing ones: Download the in-links file for the WT2g collection. The graph is in the file 'g2graph.txt'
-- Task2: Implementing and running PageRank 
		A. Implementation of the PageRank algorithm using the pseudo code provided. The code can be found in 'pagerank.py' file.
		B. Execution of the iterative version of the PageRank algorithms on the two above-mentioned graphs respectively until their PageRank values converge. To test for convergence, calculate the perplexity of the PageRank distribution using the formulae provided. 
-- Task3: Qualitative Analysis 
		Examination of the top 5 pages by PageRank and Top 5 by in-link counts for the above-mentioned graphs. Detailed speculation regarding why these pages have high PageRank values.

Language used:
Python 2.7.10

How to run this program
TASK 1:
to run the program, run the following command in command prompt:
python task1_makegraph.py

This code will make a graph of my previous 1000 crawled links from assignment1. It takes an input from task1_crawled.txt and create a graph out of all the links.

If you wish to change the seed link then you will have to open the source code and make changes to the constant: in_file



Task 2:
to run the program, run the following command in command prompt:
python task2_pagerank.py

If you wish to find the Pagerank of different graphs then you need to change the variable 'inlink_file' to either of 'g1graph.txt', 'g2graph.txt' or 'abcgraph.txt'.






