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
        max_iter: int,
        max_iter_per_t: int,
        random_state: int,
        cooling: Literal["linear", "exp", "log"],
        max_blocks: int,
        neighbor_weights: list[float],
        visited: set[str],
    ):
        # 焼きなまし法のための変数
        self.start_temp = start_temp
        self.end_temp = end_temp if end_temp > 0 else 1e-12
        self.max_iter = max_iter
        self.max_iter_per_t = max_iter_per_t
        self.cooling = cooling
        random.seed(random_state)

        # 状態遷移関数の管理
        self.max_blocks = max_blocks
        self.neighbor_weights = neighbor_weights
        self.neighbor_funcs = (
            self._swap_adjacent_words,
            self._swap_random_words,
            self._random_insertion,
            self._swap_random_subsequences,
            self._reorder_random_blocks,
        )
        if len(self.neighbor_funcs) != len(self.neighbor_weights):
            raise ValueError("len(neighbor_funcs) != len(neighbor_weights)")
        self.visited = visited  # 山登りのために記録

    def _swap_adjacent_words(self, solution):
        """隣接する2単語を入れ替え"""
        neighbor = solution.copy()
        i = random.randint(0, len(neighbor) - 2)
        neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
        return neighbor

    def _swap_random_words(self, solution):
        """ランダムな2単語を入れ替え"""
        neighbor = solution.copy()
        i, j = random.sample(range(len(neighbor)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def _random_insertion(self, solution):
        """ランダムに範囲を抜き取り再挿入 (Insertion)"""
        neighbor = solution.copy()
        i = random.randrange(len(neighbor))
        word = neighbor.pop(i)
        j = random.randrange(len(neighbor) + 1)
        neighbor.insert(j, word)
        return neighbor

    def _swap_random_subsequences(self, solution):
        """ランダムな二つ範囲を入れ替え"""
        n = len(solution)

        while True:
            a_start = random.randrange(n)
            a_end = random.randrange(a_start + 1, n + 1)  # a_start < a_end

            b_start = random.randrange(n)
            b_end = random.randrange(b_start + 1, n + 1)  # b_start < b_end

            # 重ならないようにチェック
            if a_end <= b_start or b_end <= a_start:
                break

        if b_start < a_start:
            a_start, a_end, b_start, b_end = b_start, b_end, a_start, a_end

        # ここまでくれば必ず a_start < b_start
        part_before_A = solution[:a_start]
        A_part = solution[a_start:a_end]
        middle = solution[a_end:b_start]
        B_part = solution[b_start:b_end]
        part_after_B = solution[b_end:]

        neighbor = part_before_A + B_part + middle + A_part + part_after_B
        return neighbor

    def _reorder_random_blocks(self, solution):
        """単語列を複数のブロックに分割し、それを並べ替える"""

        copied_sol = solution.copy()

        # 1〜max_blocks の中から適当にブロック数を決める
        blocks_count = random.randint(2, min(self.max_blocks, len(copied_sol)))

        # 境界のインデックスをランダムに選んでソート
        boundaries = sorted(random.sample(range(1, len(copied_sol)), blocks_count - 1))

        # 決定した境界に従ってブロックを抽出
        blocks = []
        start_idx = 0
        for b in boundaries:
            blocks.append(copied_sol[start_idx:b])
            start_idx = b
        blocks.append(copied_sol[start_idx:])  # 最後のブロック

        # ブロックの並べ替え
        random.shuffle(blocks)

        # 再度つなぎ合わせる
        neighbor = []
        for block in blocks:
            neighbor.extend(block)

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
        current_energy = scorer.get_perplexity(" ".join(current_solution))
        current_temp = self.start_temp
        best_solution = current_solution.copy()
        best_energy = current_energy

        Tfactor = -np.log(self.start_temp / self.end_temp)
        log_temperatures = [current_temp]
        log_energies = [current_energy]

        for iter in tqdm(range(self.max_iter)):
            for _ in range(self.max_iter_per_t):

                # 近傍解を生成
                neighbor_func = self._choose_neighbor_function()
                new_solution = neighbor_func(current_solution)
                new_text = " ".join(new_solution)
                self.visited.add(new_text)
                new_energy = scorer.get_perplexity(new_text)

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


params = {
    "start_temp": 50,
    "end_temp": 5,
    "max_iter": 100,
    "max_iter_per_t": 1000,
    "random_state": 57,
    "cooling": "exp",  # Literal["linear", "exp", "log"]
    "max_blocks": 3,
    "neighbor_weights": [0.3, 0.3, 0.2, 0.1, 0.1],  #
    "visited": visited,
}
optimizer = SimulatedAnnealing(**params)
