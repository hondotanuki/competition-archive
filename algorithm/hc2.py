import random


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
        neighbor_applications: int = 2,
    ):
        self.max_iterations = max_iterations
        random.seed(random_state)
        self.neighbor_funcs = [
            self._neighbor_insertion,
            self._neighbor_block_move,
            self._swap_two_random_ranges,
            self._swap_and_shuffle_two_random_ranges,
        ]

        self.visited = visited
        # 未到達近傍解の探索上限
        self.generation_attempts = generation_attempts
        # 近傍生成関数の適用回数
        self.neighbor_applications = neighbor_applications

    def _neighbor_insertion(self, solution):
        """ある単語を抜き取り、別のランダムな位置に挿入 (Insertion)"""
        neighbor = solution.copy()
        i = random.randrange(len(neighbor))
        word = neighbor.pop(i)
        j = random.randrange(len(neighbor) + 1)
        neighbor.insert(j, word)
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

        for _ in range(self.max_iterations):
            for _ in range(self.generation_attempts):
                candidate_solution = current_solution.copy()
                for _ in range(self.neighbor_applications):
                    neighbor_func = random.choice(self.neighbor_funcs)
                    candidate_solution = neighbor_func(candidate_solution)
                candidate_text = " ".join(candidate_solution)
                if candidate_text not in self.visited:
                    self.visited.add(candidate_text)
                    break

            candidate_energy = scorer.get_perplexity(candidate_text)

            if candidate_energy < current_energy:
                current_solution = candidate_solution
                current_energy = candidate_energy
                print(f"neighbor_func: {neighbor_func}")
                print(f"current_energy: {current_energy}")

            # log
            log_energies.append(current_energy)

        return " ".join(current_solution), current_energy, log_energies


params = {"max_iterations": 20000, "random_state": 57, "generation_attempts": 1000}
optimizer = HillClimbing(**params)
optimizer.solve()
