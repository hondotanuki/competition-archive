import math
import random
from tqdm import tqdm
from typing import Literal
import numpy as np
from collections import defaultdict
import pickle
import matplotlib.pyplot as plt


class A:
    def get_perplexity():
        pass


scorer = A
visited = set()


class SimulatedAnnealing:
    def __init__(
        self,
        start_temp: int | float,
        end_temp: int | float,
        cooling: Literal["linear", "exp", "log", "manual"],
        max_iter: int,
        max_iter_per_t: int,
        neighbor_range: int,
        neighbor_weights: list[int | float],
        visited: set[str],
        batch_size: int = 4,
        random_state: int = 57,
    ):
        # 焼きなまし法のための変数
        self.start_temp = start_temp
        self.end_temp = end_temp if end_temp > 0 else 1e-12
        self.cooling = cooling

        # ranges
        self.max_iter = max_iter
        self.max_iter_per_t = max_iter_per_t
        self.neighbor_range = neighbor_range

        # 状態遷移関数の管理
        self.neighbor_weights = neighbor_weights
        self.neighbor_funcs = (
            self._swap_random_words,
            self._random_range_insertion,
            self._shift_random_range_forward,
        )
        if len(self.neighbor_funcs) != len(self.neighbor_weights):
            raise ValueError("neighbor_weightsの要素数が不正です")

        self.visited = visited

        self.batch_size = batch_size
        random.seed(random_state)

    def _swap_random_words(self, neighbor):
        """ランダムな2単語を入れ替え"""
        i, j = random.sample(range(len(neighbor)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

    def _random_range_insertion(self, neighbor):
        """ランダムな範囲の単語列を抜き取り、再挿入"""
        range_length = random.randint(1, self.neighbor_range)
        start = random.randint(0, len(neighbor) - range_length)
        end = start + range_length
        extracted = neighbor[start:end]
        del neighbor[start:end]
        insert_at = random.randint(0, len(neighbor))
        neighbor[insert_at:insert_at] = extracted

    def _shift_random_range_forward(self, neighbor):
        """ランダムな範囲の単語列をシフト"""
        range_length = random.randint(1, self.neighbor_range)
        start = random.randint(0, len(neighbor) - range_length)
        end = start + range_length - 1
        neighbor[start : end + 1] = [neighbor[end]] + neighbor[start:end]

    def _choose_neighbor_function(self):
        """定義した重みに基づいて状態遷移関数をランダム選択"""
        # k=1 で要素を1つだけ選ぶ（戻り値はリストなので [0] で取り出す）
        chosen_func = random.choices(
            self.neighbor_funcs, weights=self.neighbor_weights, k=1
        )[0]
        return chosen_func

    def _acceptance_probability(self, current_energy, new_energy, temperature):
        """焼きなまし法の受容確率"""
        if new_energy < current_energy:
            return 1.0
        return math.exp((current_energy - new_energy) / temperature)

    def solve(self, text):
        current_solution = text.split()
        if self.neighbor_range > len(current_solution) or self.neighbor_range < 0:
            raise ValueError("neighbor_rangeが不正な値です")

        current_energy = scorer.get_perplexity(
            " ".join(current_solution), self.batch_size
        )
        current_temp = self.start_temp
        best_solution = current_solution.copy()
        best_energy = current_energy

        Tfactor = -np.log(self.start_temp / self.end_temp)
        log_energies = [current_energy]
        log_per_temp = defaultdict(list)

        for iter in tqdm(range(self.max_iter)):
            for _ in range(self.max_iter_per_t):
                # 近傍解を生成
                new_solution = current_solution.copy()
                neighbor_func = self._choose_neighbor_function()
                neighbor_func(new_solution)
                new_text = " ".join(new_solution)
                self.visited.add(new_text)
                new_energy = scorer.get_perplexity(new_text, self.batch_size)
                # new_energy = scorer.get_perplexity(new_text)

                acceptance = self._acceptance_probability(
                    current_energy, new_energy, current_temp
                )
                if acceptance > random.random():
                    current_solution = new_solution
                    current_energy = new_energy

                # 解の更新
                if new_energy < best_energy:
                    best_solution = new_solution.copy()
                    best_energy = new_energy
                    print(f"best_score!!!!!: {best_energy}")

                # log
                log_energies.append(current_energy)
                log_per_temp[current_temp].append(current_energy)

            # 温度減少関数
            if self.cooling == "linear":
                current_temp -= (self.start_temp - self.end_temp) / self.max_iter
            elif self.cooling == "exp":
                current_temp = self.start_temp * math.exp(
                    Tfactor * (iter + 1) / self.max_iter
                )
            elif self.cooling == "log":
                current_temp = self.start_temp / math.log10(iter + 10)

        return " ".join(best_solution), best_energy, log_energies, log_per_temp

    # start_temp: int,
    # end_temp: int,
    # cooling: Literal["linear", "exp", "log"],
    # max_iter: int,
    # max_iter_per_t: int,
    # neighbor_application: int,
    # neighbor_weights: list[float],
    # batch_size: int,
    # random_state: int,
    # visited: set[str],
    # text = df.loc[id_, "score"]


params = {
    "start_temp": 0.5,
    "end_temp": 0.1,
    "cooling": "exp",  # Literal["linear", "exp", "log"]
    "max_iter": 2,
    "max_iter_per_t": 10000,
    "max_range": 6,
    "neighbor_weights": [1, 3, 2],
    "visited": visited,
    "batch_size": 4,
    "random_state": 57,
}
optimizer = SimulatedAnnealing(**params)

df = None
log = dict()
for id_ in [3, 4, 5]:
    with open(f"/kaggle/input/input-data/visited_{id_}.pkl", mode="rb") as f:
        visited = pickle.load(f)
    params = {
        "start_temp": 10,
        "end_temp": 0.1,
        "cooling": "linear",  # Literal["linear", "exp", "log"]
        "max_iter": 20,
        "max_iter_per_t": 1000,
        "neighbor_range": 5,
        "neighbor_weights": [1, 3, 2],
        "visited": visited,
        "batch_size": 4,
        "random_state": 57,
    }
    optimizer = SimulatedAnnealing(**params)
    cur_text = df.loc[id_, "text"]
    cur_score = df.loc[id_, "score"]
    text, score, log_scores, log_score_per_t = optimizer.solve(cur_text)
    log[id_] = log_score_per_t
    if score < cur_score:
        df.loc[id_, "text"] = text
        df.loc[id_, "score"] = score
    with open(f"/kaggle/working/logtexts_{id_}.pkl", mode="wb") as f:
        pickle.dump(visited, f)

    plt.plot(log_scores)
    plt.title(f'id = {id_}, start_temp = {params["start_temp"]}')
    plt.xlabel("iteration")
    plt.ylabel("score")
    plt.show()
