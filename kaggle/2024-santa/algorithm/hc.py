import random
from typing import Literal
from tqdm import tqdm


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
        visited: set[str],
        function_selector: list[
            Literal[
                "swap",
                "insertion",
                "reverse",
                "block",
                "swap_block",
                "swap_shuffle_block",
            ]
        ],
    ):
        self.max_iterations = max_iterations
        random.seed(random_state)

        # 状態遷移関数管理
        neighbor_all = {
            "swap": self._neighbor_swap,
            "insertion": self._neighbor_insertion,
            "reverse": self._neighbor_reverse,
            "block": self._neighbor_block_move,
            "swap_block": self._swap_two_random_ranges,
            "swap_shuffle_block": self._swap_and_shuffle_two_random_ranges,
        }
        self.neighbor_funcs = []
        for k in function_selector:
            self.neighbor_funcs.append(neighbor_all[k])
        assert self.neighbor_funcs, "状態遷移関数が定義されていない"

        # 文字列の再探索対策
        self.visited = visited
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

    def _swap_two_random_ranges(self, solution):
        """ランダムな二つの範囲の要素を入れ替え"""
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

    def _swap_and_shuffle_two_random_ranges(self, solution):
        """ランダムな二つの範囲の要素をシャッフルし入れ替え"""

        n = len(solution)
        while True:
            start1 = random.randrange(n)
            end1 = random.randrange(start1 + 1, n + 1)
            start2 = random.randrange(n)
            end2 = random.randrange(start2 + 1, n + 1)
            (front_start, front_end), (back_start, back_end) = sorted(
                [(start1, end1), (start2, end2)], key=lambda x: x[0]
            )

            # 重ならないならループを抜ける
            if front_end <= back_start:
                break
        front_part = solution[front_start:front_end]
        back_part = solution[back_start:back_end]

        # 範囲内の要素をランダムに並び替え
        random.shuffle(front_part)
        random.shuffle(back_part)

        # front と back を入れ替え
        neighbor = (
            solution[:front_start]
            + back_part
            + solution[front_end:back_start]
            + front_part
            + solution[back_end:]
        )

        return neighbor

    def solve(self, text):
        current_solution = text.split()
        current_energy = scorer.get_perplexity(" ".join(current_solution))

        log_energies = [current_energy]

        for _ in tqdm(range(self.max_iterations)):
            # generate neighbor
            for _ in range(self.generation_attempts):
                neighbor_func = random.choice(self.neighbor_funcs)
                new_solution = neighbor_func(current_solution)
                new_text = " ".join(new_solution)
                if new_text not in self.visited:
                    self.visited.add(new_text)
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
