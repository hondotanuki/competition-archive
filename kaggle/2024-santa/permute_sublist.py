from itertools import permutations as perm
import pandas as pd


class A:
    def get_perplexity(self, text):
        return len(text)


scorer = A()


def permute_sublist(lst, start, end):
    """
    リストの指定範囲 [start, end) を全ての順列に並び替えたリストを生成
    8!=40320まで、それ以降は計算量が重い
    """
    assert 0 < end - start < 9, "不当なインデックス"
    sublist = lst[start:end]
    permuted_sublists = list(perm(sublist))

    solutions = []
    for sublist in permuted_sublists:
        new_solution = lst[:start] + list(sublist) + lst[end:]
        solutions.append(new_solution)

    return solutions


i = 0
start = 5
end = 10


df = pd.read_csv("")
original_list = df.loc[i, "text"].split()
best_score = df.loc[i, "score"]
solutions = permute_sublist(original_list, start, end)
for solution in solutions:
    text = " ".join(solution)
    score = scorer.get_perplexity(text)
    if score < best_score:
        best_text = text
        best_score = score
        print(f"Best score!!!!: {best_score}")

print(best_score, best_text)
