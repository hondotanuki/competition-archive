import pickle
import numpy as np
import pandas as pd


class A:
    def get_perplexity():
        pass


scorer = A
visited = set()


class BeamSearch:
    def __init__(self, max_iterations, init_text=""):
        self.init_text = init_text

    def _make_candidates_adding_word(self, current_text, words):
        """Make candidate text so that word duplication does not occur"""
        candidates = []
        not_used_words = words.copy()
        for used_word in current_text.split():
            not_used_words.remove(used_word)

        candidates += [(current_text + " " + word).lstrip() for word in not_used_words]

        return candidates

    def solve(self, text):
        n_text = len(text.split())
        if n_text > 100:
            raise "長すぎ"
        current_texts = [self.init_text]
        words = list(set(text.split()) - set(self.init_text.split()))

        # 2*10^4程度の計算量へ調整
        beam_width = min(40000 // (len(words) * (len(words) + 1)), n_text)

        while len(current_texts[0].split()) < n_text:
            candidates = []
            for current_text in current_texts:
                candidates += self._make_candidates_adding_word(current_text, words)

            candidates = list(set(candidates))  # drop duplicate

            scores = scorer.get_perplexity(candidates)
            top_idx = sorted(range(len(scores)), key=lambda i: scores[i])[:beam_width]
            current_texts = [candidates[i] for i in top_idx]

        best_score = min(scores)
        best_text = candidates[np.argmin(scores)]

        return best_score, best_text


with open("/content/drive/MyDrive/kaggle/input/pickle/blocks.pkl", mode="rb") as f:
    block = pickle.load(f)
df = pd.read_csv("/content/drive/MyDrive/kaggle/input/csv/202511_12.csv")

i = 3
text = df.loc[i, "text"]
init_text = block[i][0][2]

optimizer = BeamSearch(init_text)
best_score, best_text = optimizer.solve(text)
