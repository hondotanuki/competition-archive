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
        max_range: int,
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

        # 近傍生成関連
        self.max_range = max_range
        self.neighbor_funcs = (
            self._swap_random_words,
            self._random_range_insertion,
            self._shift_random_range_forward,
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

    def _random_range_insertion(self, neighbor):
        """ランダムな範囲の単語列を抜き取り、再挿入"""
        range_length = random.randint(1, self.max_range)
        start = random.randint(0, len(neighbor) - range_length)
        end = start + range_length
        extracted = neighbor[start:end]
        del neighbor[start:end]
        insert_at = random.randint(0, len(neighbor))
        neighbor[insert_at:insert_at] = extracted

    def _shift_random_range_forward(self, neighbor):
        """ランダムな範囲の単語列をシフト"""
        start = random.randint(0, len(neighbor) - 2)
        end = random.randint(start + 1, len(neighbor) - 1)
        neighbor[start : end + 1] = [neighbor[end]] + neighbor[start:end]

    def _choose_neighbor_function(self):
        """定義した重みに基づいて状態遷移関数をランダム選択"""
        # k=1 で要素を1つだけ選ぶ（戻り値はリストなので [0] で取り出す）
        chosen_func = random.choices(
            self.neighbor_funcs, weights=self.neighbor_weights, k=1
        )[0]
        return chosen_func

    def solve(self, text):
        current_solution = text.split()
        # current_energy = scorer.get_perplexity(
        #     " ".join(current_solution), self.batch_size
        # )
        current_energy = scorer.get_perplexity(" ".join(current_solution))

        log_energies = [current_energy]

        for iter in tqdm(range(self.max_iter)):
            # generate neighbor
            for attempts in range(self.max_attempts):
                new_solution = current_solution.copy()
                for _ in range(random.randint(1, self.neighbor_application)):
                    neighbor_func = self._choose_neighbor_function()
                    neighbor_func(new_solution)
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

        return " ".join(current_solution), current_energy, log_energies


params = {
    "max_iter": 100,
    "max_attempts": 10000,
    "max_rannge": 6,
    "neighbor_application": 8,
    "neighbor_weights": [1, 3, 2],
    "batch_size": 1024,
    "random_state": 57,
    "visited": visited,
}
optimizer = HillClimbing(**params)


# def _shift_random_range_backward(self, neighbor):
#     """ランダムな範囲の単語列をシフト(先頭要素を末尾へ移動)"""
#     start = random.randint(0, len(neighbor) - 2)
#     end = random.randint(start + 1, len(neighbor) - 1)
#     # 先頭要素 neighbor[start] を最後に移動
#     neighbor[start : end + 1] = neighbor[start + 1 : end + 1] + [neighbor[start]]
