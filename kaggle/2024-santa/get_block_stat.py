from collections import defaultdict
from sortedcontainers import SortedList

words = [chr(i) for i in range(65, 76)]
n = len(words)
d = defaultdict(SortedList)
for i in range(n):
    for j in range(i + 1, n + 1):
        text = " ".join(words[i:j])
        score = scorer.get_perplexity(text)
        d[j - i].add((score, text))
