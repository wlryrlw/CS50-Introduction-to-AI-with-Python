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
    distribution = dict()
    pages = list(corpus.keys())
    n_pages = len(pages)

    # If page has no outgoing links, treat it as linking to all pages
    links = corpus.get(page, set())
    if len(links) == 0:
        for p in pages:
            distribution[p] = 1 / n_pages
        return distribution

    # Base probability of choosing any page at random
    for p in pages:
        distribution[p] = (1 - damping_factor) / n_pages

    # Add damping probability distributed among linked pages
    for linked_page in links:
        distribution[linked_page] += damping_factor / len(links)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    pages = list(corpus.keys())
    counts = {p: 0 for p in pages}

    current = random.choice(pages)
    counts[current] += 1

    for _ in range(1, n):
        distribution = transition_model(corpus, current, damping_factor)
        next_pages = list(distribution.keys())
        weights = [distribution[p] for p in next_pages]
        current = random.choices(next_pages, weights=weights, k=1)[0]
        counts[current] += 1

    return {p: counts[p] / n for p in pages}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    n_pages = len(pages)
    threshold = 0.001

    ranks = {p: 1 / n_pages for p in pages}

    incoming = {p: set() for p in pages}
    for p in pages:
        for linked in corpus[p]:
            incoming[linked].add(p)

    while True:
        new_ranks = dict()

        for p in pages:
            rank = (1 - damping_factor) / n_pages

            total = 0
            for i in incoming[p]:
                num_links = len(corpus[i])
                if num_links == 0:
                    
                    total += ranks[i] / n_pages
                else:
                    total += ranks[i] / num_links

            rank += damping_factor * total
            new_ranks[p] = rank

        deltas = [abs(new_ranks[p] - ranks[p]) for p in pages]
        ranks = new_ranks
        if max(deltas) < threshold:
            break

    s = sum(ranks.values())
    return {p: ranks[p] / s for p in pages}


if __name__ == "__main__":
    main()
