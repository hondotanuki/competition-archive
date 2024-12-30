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
        self.neighbor_funcs = [self._neighbor_insertion, self._neighbor_block_move]

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
