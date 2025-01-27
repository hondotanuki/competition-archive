import random
from tqdm import tqdm


class A:
    def get_perplexity():
        pass


scorer = A
visited = set()


class HillClimbing:
    def __init__(
        self,
        max_iter: int,
        random_state: int,
        generation_attempts: int,
        max_blocks: int,
        neighbor_weights: list[float],
        visited: set[str],
    ):
        self.max_iter = max_iter
        random.seed(random_state)

        # 未到達近傍解の探索上限
        self.generation_attempts = generation_attempts

        # 近傍生成関数の適用回数
        self.max_blocks = max_blocks
        self.neighbor_weights = neighbor_weights
        self.neighbor_funcs = (
            self._swap_adjacent_words,
            self._swap_random_words,
            self._random_insertion,
            self._swap_random_subsequences,
            self._reorder_random_blocks,
            self._swap_and_shuffle_two_random_ranges,
        )
        self.visited = visited

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

    def _choose_neighbor_function(self):
        """定義した重みに基づいて状態遷移関数をランダム選択"""
        # k=1 で要素を1つだけ選ぶ（戻り値はリストなので [0] で取り出す）
        chosen_func = random.choices(
            self.neighbor_funcs, weights=self.neighbor_weights, k=1
        )[0]
        return chosen_func

    def solve(self, text):
        current_solution = text.split()
        current_energy = scorer.get_perplexity(" ".join(current_solution))

        log_energies = [current_energy]

        for iter in tqdm(range(self.max_iter)):
            # generate neighbor
            # for _ in range(self.generation_attempts):
            while True:
                neighbor_func = self._choose_neighbor_function()
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
                print(f"best_energy!!!: {current_energy}")

            # log
            log_energies.append(new_energy)

        return " ".join(current_solution), current_energy, log_energies, _


params = {
    "max_iter": 100,
    "random_state": 57,
    "generation_attempts": 1000,
    "max_blocks": 3,
    "neighbor_weights": [0.3, 0.3, 0.2, 0.1, 0.1],  #
    "visited": visited,
}
optimizer = HillClimbing(**params)
