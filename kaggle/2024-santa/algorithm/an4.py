import math
import random
from tqdm import tqdm
from typing import Literal
import numpy as np


class A:
    def get_perplexity():
        pass


scorer = A
visited = set()


class SimulatedAnnealing:
    def __init__(
        self,
        start_temp: int,
        end_temp: int,
        cooling: Literal["linear", "exp", "log"],
        max_iter: int,
        max_iter_per_t: int,
        neighbor_application: int,
        neighbor_weights: list[float],
        batch_size: int,
        random_state: int,
        visited: set[str],
    ):
        # 焼きなまし法のための変数
        self.start_temp = start_temp
        self.end_temp = end_temp if end_temp > 0 else 1e-12
        self.cooling = cooling
        self.max_iter = max_iter
        self.max_iter_per_t = max_iter_per_t
        self.neighbor_application = neighbor_application

        # 状態遷移関数の管理
        self.neighbor_weights = neighbor_weights
        self.neighbor_funcs = (
            self._swap_random_words,
            self._random_insertion,
            self._shift_random_range,
        )
        if len(self.neighbor_funcs) != len(self.neighbor_weights):
            raise ValueError("len(neighbor_funcs) != len(neighbor_weights)")

        self.batch_size = batch_size
        random.seed(random_state)
        self.visited = visited  # 山登りのために記録

    def _swap_random_words(self, neighbor):
        """ランダムな2単語を入れ替え"""
        i, j = random.sample(range(len(neighbor)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def _random_insertion(self, neighbor):
        """ランダムに範囲を抜き取り再挿入 (Insertion)"""
        i = random.randrange(len(neighbor))
        word = neighbor.pop(i)
        j = random.randrange(len(neighbor) + 1)
        neighbor.insert(j, word)
        return neighbor

    def _shift_random_range(self, neighbor):
        """ランダムな範囲の単語列をシフト"""
        start = random.randint(0, len(neighbor) - 2)
        end = random.randint(start + 1, len(neighbor) - 1)
        neighbor[start : end + 1] = [neighbor[end]] + neighbor[start:end]

        return neighbor

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
        current_energy = scorer.get_perplexity(
            " ".join(current_solution), self.batch_size
        )
        current_temp = self.start_temp
        best_solution = current_solution.copy()
        best_energy = current_energy

        Tfactor = -np.log(self.start_temp / self.end_temp)
        log_temperatures = [current_temp]
        log_energies = [current_energy]

        for iter in tqdm(range(self.max_iter)):
            for _ in range(self.max_iter_per_t):
                # 近傍解を生成
                new_solution = current_solution.copy()
                for _ in range(random.randint(1, self.neighbor_application)):
                    neighbor_func = self._choose_neighbor_function()
                    new_solution = neighbor_func(new_solution)
                new_text = " ".join(new_solution)
                self.visited.add(new_text)
                new_energy = scorer.get_perplexity(new_text, self.batch_size)

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
                    print(f"neighbor_func: {neighbor_func}")
                    print(f"best_score!!!!!: {best_energy}")

                # log
                log_energies.append(current_energy)
                log_temperatures.append(current_temp)

            # 温度減少関数
            if self.cooling == "linear":
                current_temp -= (self.start_temp - self.end_temp) / self.max_iter
            elif self.cooling == "exp":
                current_temp = self.start_temp * math.exp(
                    Tfactor * (iter + 1) / self.max_iter
                )
            elif self.cooling == "log":
                current_temp = self.start_temp / math.log10(iter + 10)

        return " ".join(best_solution), best_energy, log_energies, log_temperatures


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

params = {
    "start_temp": 5,
    "end_temp": 0.2,
    "cooling": "exp",  # Literal["linear", "exp", "log"]
    "max_iter": 100,
    "max_iter_per_t": 1000,
    "neighbor_application": 5,
    "neighbor_weights": [0.3, 0.3, 0.2],
    "batch_size": 1024,
    "random_state": 57,
    "visited": visited,
}
optimizer = SimulatedAnnealing(**params)
