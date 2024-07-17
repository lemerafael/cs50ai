import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    output = {}
    pageLinks = corpus[page]
    linksCount = len(pageLinks)
    if linksCount == 0:
        pageLinks = list(corpus.keys())
        linksCount = len(pageLinks)
    linking_prob = damping_factor / linksCount
    for link in pageLinks:
        output[link] = add_if_valid(output.get(link), linking_prob)
    pagesCount = len(corpus)
    pages_prob = (1 - damping_factor) / pagesCount
    for link in corpus:
        output[link] = add_if_valid(output.get(link), pages_prob)
    return output


def add_if_valid(current, new):
    output = 0
    if (current is None):
        current = 0
    output = current + new
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = random.choice(list(corpus.keys()))
    index = 1
    sampling = {}
    while index < n:
        tm = transition_model(corpus, sample, damping_factor)
        sampling[sample] = add_if_valid(sampling.get(sample), 1)
        index = index + 1
        sample = random.choices(list(tm.keys()), weights=list(tm.values()))[0]
    for sample in list(sampling.keys()):
        sampling[sample] = sampling[sample] / n
    return sampling


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagesCount = len(corpus)
    pageRanks = init_corpus_map(corpus.keys(), 1 / pagesCount)
    shouldStop = False
    MIN_DELTA = 0.001
    while (shouldStop == False):
        shouldStop = True
        for page in list(pageRanks.keys()):
            new_rank = (1-damping_factor) / pagesCount
            linkSum = 0
            pagesThatLink = get_pages_that_link(corpus, page)
            numLinks = pagesCount
            for linked in pagesThatLink:
                numLinksCount = len(corpus[linked])
                if numLinksCount > 0:
                    numLinks = numLinksCount
                linkSum = linkSum + pageRanks[linked] / numLinks
            new_rank = new_rank + damping_factor * linkSum
            if (abs(pageRanks[page] - new_rank) > MIN_DELTA):
                shouldStop = False
            pageRanks[page] = new_rank
    return pageRanks


def init_corpus_map(corpus, value):
    output = {}
    for link in corpus:
        output[link] = add_if_valid(0, value)
    return output


def get_pages_that_link(corpus, page):
    output = []
    for index in corpus:
        if page in corpus[index] or len(corpus[index]) == 0:
            output.append(index)
    return output


if __name__ == "__main__":
    main()
