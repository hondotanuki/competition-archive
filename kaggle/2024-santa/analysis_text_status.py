import pandas as pd
import matplotlib as plt


class A:
    def get_perplexity(self, text):
        return len(text)


scorer = A()

# 現在の文章に単語を追加していったときのスコアの増減をみる
# 明らかに増分が多い場所は間違っているのではないか、などの推察目的
df = pd.read_csv("")
for i in range(6):
    words = df.loc[i, "text"].split()
    n = len(words)
    log_scores = []
    for i in range(1, n + 1):
        text = " ".join(words[:i])
        score = scorer.get_perplexity(text)
        log_scores.append(score)

    plt.plot(log_scores)
    plt.title(f"id = {i}, num of word = {n}")
    plt.xlabel("iteration")
    plt.ylabel("score")
    plt.show()
