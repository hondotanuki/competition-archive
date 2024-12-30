import random
from typing import Literal


class A:
    def get_perplexity():
        pass


scorer = A


class HillClimbing:
    def __init__(
        self,
        max_iterations: int,
        random_state: int,
        generation_attempts: int,
        function_selector: list[Literal["swap", "insertion", "reverse", "block"]],
    ):
        self.max_iterations = max_iterations
        random.seed(random_state)

        # 状態遷移関数管理
        neighbor_all = {
            "swap": self._neighbor_swap,
            "insertion": self._neighbor_insertion,
            "reverse": self._neighbor_reverse,
            "block": self._neighbor_block_move,
        }
        self.neighbor_funcs = []
        for k in function_selector:
            self.neighbor_funcs.append(neighbor_all[k])
        print()
        assert self.neighbor_funcs, "状態遷移関数が定義されていない"

        # 文字列の再探索対策
        self.generation_attempts = generation_attempts  # 山登り法用

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

    def solve(self, text, visited):
        current_solution = text.split()
        current_energy = scorer.get_perplexity(" ".join(current_solution))

        log_energies = [current_energy]

        for _ in range(self.max_iterations):
            # generate neighbor
            for _ in range(self.generation_attempts):
                neighbor_func = random.choice(self.neighbor_funcs)
                new_solution = neighbor_func(current_solution)
                new_text = " ".join(new_solution)
                if new_text not in visited:
                    visited.add(new_text)
                    break
            new_energy = scorer.get_perplexity(new_text)

            # update solution
            if new_energy < current_energy:
                current_solution = new_solution.copy()
                current_energy = new_energy
                print(f"neighbor_func: {neighbor_func}")
                print(f"current_energy: {current_energy}")

            # log
            log_energies.append(current_energy)

        return " ".join(current_solution), current_energy, log_energies


# function_selector: list[Literal["swap", "insertion", "reverse", "block"]]
params = {
    "max_iterations": 20000,
    "random_state": 42,
    "generation_attempts": 1000,
    "function_selector": ["swap", "insertion", "reverse", "block"],
}
visited = set()
optimizer = HillClimbing(**params)
optimizer.solve(visited)
