import numpy as np
from tqdm import tqdm


class A:
    def get_perplexity(texts: list[str]):
        return [len(text) for text in texts]


scorer = A
visited = set()


class BeamSearch:
    def __init__(self, beam_width: int, init_text: str = ""):
        self.beam_width = beam_width
        self.init_text = init_text

    def _make_candidates_adding_word(self, current_text, words):
        """Make candidate text so that word duplication does not occur"""
        candidates = []
        not_used_words = words.copy()
        for used_word in current_text.split():
            not_used_words.remove(used_word)

        candidates += [(current_text + " " + word).lstrip() for word in not_used_words]
        candidates += [(word + " " + current_text).rstrip() for word in not_used_words]

        return candidates

    def _make_candiates_by_insertion(self, current_text, words):
        """Make candidate text so that word duplication does not occur"""
        tokens = current_text.split()

        # current_text ですでに使われている単語は除外
        not_used_words = [w for w in words if w not in tokens]

        candidates = []
        # 挿入箇所はトークンの間 ＋ 先頭 ＋ 末尾 で合計 len(tokens) + 1 箇所
        for i in range(len(tokens) + 1):
            for w in not_used_words:
                # i番目の位置に w を挿入
                new_tokens = tokens[:i] + [w] + tokens[i:]
                new_text = " ".join(new_tokens)
                candidates.append(new_text)

        return candidates

    def _calc_cost(self, n: int):
        return n * (n + 1) * (n + 2) // 6 * self.beam_width

    def solve(self, text):
        words = text.split()
        current_texts = [self.init_text]

        cost1 = self._calc_cost(len(words))
        cost2 = self._calc_cost(len(self.init_text.split()))
        cost = cost1 - cost2
        assert cost < 50000, f"計算量が多すぎます。{cost=}"
        print(f"{cost=}")

        # 2*10^4程度の計算量へ調整
        # 重複や最初の処理量により多めに計算されている
        # beam_width = min(2 * self.max_iterations // (n_init * (n_init + 1)), n_text)
        # print(beam_width)
        with tqdm() as pbar:
            while len(current_texts[0].split()) < len(words):
                candidates = []
                for current_text in current_texts:
                    candidates += self._make_candidates_adding_word(current_text, words)

                candidates = list(set(candidates))  # drop duplicate
                scores = scorer.get_perplexity(candidates)
                top_idx = sorted(range(len(scores)), key=lambda i: scores[i])[
                    : self.beam_width
                ]
                current_texts = [candidates[i] for i in top_idx]
                pbar.update(1)

        best_score = min(scores)
        best_text = candidates[np.argmin(scores)]

        return best_score, best_text


i = 3
# df = pd.read_csv("/content/drive/MyDrive/kaggle/input/csv/202511_12.csv")
init_text = ""
# text = df.loc[i, "text"]
text = "Key concepts to understand when working with the OpenAI API"
print(len(text.split()))
optimizer = BeamSearch(1000, init_text)
best_score, best_text = optimizer.solve(text)
print(len(best_text.split()))
