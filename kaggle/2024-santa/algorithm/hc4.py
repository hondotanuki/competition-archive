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
        max_attempts: int,
        neighbor_application: int,
        neighbor_weights: list[float],
        batch_size: int,
        random_state: int,
        visited: set[str],
    ):
        # イテレート回数
        self.max_iter = max_iter
        self.max_attempts = max_attempts
        self.neighbor_application = neighbor_application

        # 近傍生成関数の適用回数
        self.neighbor_funcs = (
            self._swap_random_words,
            self._random_insertion,
            self._shift_random_range_forward,
            self._shift_random_range_backward,
            self._swap_random_subsequences,
        )
        assert len(self.neighbor_funcs) == len(
            neighbor_weights
        ), "入力された重みが不正です"
        self.neighbor_weights = neighbor_weights

        self.batch_size = batch_size
        random.seed(random_state)
        self.visited = visited

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

    def _shift_random_range_forward(self, neighbor):
        """ランダムな範囲の単語列をシフト"""
        start = random.randint(0, len(neighbor) - 2)
        end = random.randint(start + 1, len(neighbor) - 1)
        neighbor[start : end + 1] = [neighbor[end]] + neighbor[start:end]

        return neighbor

    def _shift_random_range_backward(self, neighbor):
        """ランダムな範囲の単語列をシフト(先頭要素を末尾へ移動)"""
        start = random.randint(0, len(neighbor) - 2)
        end = random.randint(start + 1, len(neighbor) - 1)

        # 先頭要素 neighbor[start] を最後に移動
        neighbor[start : end + 1] = neighbor[start + 1 : end + 1] + [neighbor[start]]

        return neighbor

    def _swap_random_subsequences(self, neighbor):
        """ランダムな二つ範囲を入れ替え"""
        n = len(neighbor)

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

        part_before_A = neighbor[:a_start]
        A_part = neighbor[a_start:a_end]
        middle = neighbor[a_end:b_start]
        B_part = neighbor[b_start:b_end]
        part_after_B = neighbor[b_end:]

        neighbor = part_before_A + B_part + middle + A_part + part_after_B
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
        current_energy = scorer.get_perplexity(
            " ".join(current_solution), self.batch_size
        )

        log_energies = [current_energy]

        for iter in tqdm(range(self.max_iter)):
            # generate neighbor
            for attempts in range(self.max_attempts):
                new_solution = current_solution.copy()
                for _ in range(random.randint(1, self.neighbor_application)):
                    neighbor_func = self._choose_neighbor_function()
                    new_solution = neighbor_func(new_solution)
                new_text = " ".join(new_solution)
                if new_text not in self.visited:
                    self.visited.add(new_text)
                    break
                if attempts == self.max_attempts - 1:
                    print("新しい解が生成されませんでした。処理を終了します。")
                    return " ".join(current_solution), current_energy, log_energies

            # new_energy = scorer.get_perplexity(new_text, self.batch_size)
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
    "max_attempts": 10000,
    "neighbor_application": 5,
    "neighbor_weights": [1, 1, 1, 1],
    "batch_size": 1024,
    "random_state": 57,
    "visited": visited,
}
optimizer = HillClimbing(**params)
