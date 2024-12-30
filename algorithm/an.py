from math import exp
import random
from tqdm import tqdm


class A:
    def get_perplexity():
        pass


scorer = A


class SimulatedAnnealing:
    def __init__(
        self,
        start_temp: int,
        end_temp: int,
        max_iterations: int,
        random_state: int,
        phase_weights: list[float],
        phase_boundaries: list[float],
    ):
        # 焼きなまし法のための変数
        self.start_temp = start_temp
        self.end_temp = end_temp
        self.max_iterations = max_iterations
        random.seed(random_state)

        # 状態遷移の制御
        self.neighbor_funcs = [
            self._neighbor_swap,
            self._neighbor_insertion,
            self._neighbor_reverse,
            self._neighbor_block_move,
        ]
        self.phase_weights = phase_weights
        self.phase_boundaries = phase_boundaries

    def _neighbor_swap(self, solution):
        """ランダムな2単語を入れ替え"""
        neighbor = solution.copy()
        i, j = random.sample(range(len(neighbor)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def _neighbor_insertion(self, solution):
        """ある単語を抜き取り、別のランダムな位置に挿入 (Insertion)"""
        neighbor = solution.copy()
        i = random.randrange(len(neighbor))
        word = neighbor.pop(i)
        j = random.randrange(len(neighbor) + 1)
        neighbor.insert(j, word)
        return neighbor

    def _neighbor_reverse(self, solution):
        """部分反転 (Reverse)"""
        neighbor = solution.copy()
        i, j = sorted(random.sample(range(len(neighbor)), 2))
        neighbor[i : j + 1] = reversed(neighbor[i : j + 1])
        return neighbor

    def _neighbor_block_move(self, solution):
        """連続ブロックを取り出し別の位置に挿入 (Block Move)"""
        neighbor = solution.copy()
        i, j = sorted(random.sample(range(len(neighbor)), 2))
        block = neighbor[i : j + 1]
        del neighbor[i : j + 1]
        k = random.randrange(len(neighbor) + 1)
        for idx, w in enumerate(block):
            neighbor.insert(k + idx, w)
        return neighbor

    def _get_phase(self, step_ratio):
        """進捗率に応じたフェーズ(0,1,2...)を返す"""
        for i, boundary in enumerate(self.phase_boundaries):
            if step_ratio < boundary:
                return i
        return len(self.phase_boundaries)

    def _choose_neighbor_function(self, phase):
        """フェーズごとの重みに基づいて近傍操作を確率的に選ぶ"""
        weights = self.phase_weights[phase]
        chosen_func = random.choices(self.neighbor_funcs, weights=weights, k=1)[0]
        return chosen_func

    def _acceptance_probability(self, current_energy, new_energy, temperature):
        """焼きなまし法の受容確率"""
        if new_energy < current_energy:
            return 1.0
        return exp((current_energy - new_energy) / temperature)

    def _lower_temperature(self, temperature):
        """線形に温度を下げる"""
        return temperature - ((self.start_temp - self.end_temp) / self.max_iterations)

    def solve(self, text):
        current_solution = text.split()
        current_energy = scorer.get_perplexity(" ".join(current_solution))
        best_solution = current_solution.copy()
        best_energy = current_energy

        temperature = self.start_temp
        log_energies = [current_energy]

        for iteration in tqdm(range(self.max_iterations)):
            # フェーズによって近傍探索手法を変える
            step_ratio = iteration / self.max_iterations
            phase = self._get_phase(step_ratio)
            neighbor_func = self._choose_neighbor_function(phase)

            # 近傍解を生成
            new_solution = neighbor_func(current_solution)
            new_text = " ".join(new_solution)
            new_energy = scorer.get_perplexity(new_text)

            # 焼きなまし
            acceptance = self._acceptance_probability(
                current_energy, new_energy, temperature
            )
            if acceptance > random.random():
                current_solution = new_solution
                current_energy = new_energy

            # 解の更新
            if new_energy < best_energy:
                best_solution = new_solution.copy()
                best_energy = new_energy
                print(f"best_score: {neighbor_func}")
                print(f"best_score: {best_energy}")

            # 温度減少関数
            temperature = self._lower_temperature(temperature)

            # log
            log_energies.append(current_energy)

        return " ".join(best_solution), best_energy, log_energies


# swap, insert, reverse, block_move
phase_weights = [
    [0, 0, 0.5, 0.5],  # phase 0 (序盤)
    [0, 0.5, 0.5, 0],  # phase 1 (中盤)
    [0.4, 0.1, 0.1, 0.4],  # phase 2 (終盤): swap を多め
]

# フェーズ判定の閾値（ここでは3フェーズに分割する例）
#  - phase 0: [0%, 33%)   -> 序盤
#  - phase 1: [33%, 66%)  -> 中盤
#  - phase 2: [66%, 100%] -> 終盤
phase_boundaries = [0.33, 0.66]  # 境界値

params = {
    "start_temp": 50,  # 初期温度
    "end_temp": 5,  # 最終温度
    "max_iterations": 12000,  # 反復回数
    "random_state": 42,
    "phase_weights": phase_weights,
    "phase_boundaries": phase_boundaries,
}
optimizer = SimulatedAnnealing(**params)
