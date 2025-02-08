import random
from itertools import permutations as perm

solution = [chr(i) for i in range(65, 91)]
solution.sort(reverse=True)
stop_words = {
    "to",
    "not",
    "of",
    "and",
    "in",
    "with",
    "that",
    "we",
    "you",
    "as",
    "from",
    "have",
    "it",
    "the",
    "is",
}


class A:
    def get_perplexity():
        pass


scorer = A


def sort_random_range(neighbor):
    while True:
        start = random.randint(0, len(neighbor) - 1)
        end = random.randint(start + 1, len(neighbor))
        sub_range = neighbor[start:end]

        # 範囲に stop_words が含まれているかチェック
        if any(word in stop_words for word in sub_range):
            continue
        else:
            neighbor[start:end] = sorted(sub_range)
            break


def perm_random_range(neighbor):
    rlen = random.randint(2, 6)
    start = random.randint(0, len(neighbor) - rlen)

    new_score, best_score = float("inf"), float("inf")
    best_neibhor = None
    sub_range = neighbor[start : start + rlen]
    for p in perm(sub_range, rlen):
        new_neighbor = neighbor[:start] + [*p] + neighbor[start + rlen :]
        new_text = " ".join(new_neighbor)
        new_score = scorer.get_perplexity(new_text, 4)
        if new_score < best_score:
            best_score = new_score
            best_neibhor = new_neighbor.copy()
    return best_neibhor


# print(solution)
# sort_random_range(solution)
solution = [1, 2, 3]
perm_with_random_range(solution)
