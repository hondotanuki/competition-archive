import random
import time

# input
n, m, t = map(int, input().split())
n_x = 2 * n * (n - 1)
dij = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def calc_score(tanes: list[list[int]]) -> int:
    assert len(tanes) == n_x, f"len: {len(tanes)}"
    return max(sum(tane) for tane in tanes)


def get_screened_tanes_idx() -> list[int]:
    screened_tanes_idx = random.sample(range(n_x), n**2)
    return screened_tanes_idx


def gen_field(screened_tanes_idx: list[int]) -> list[list[int]]:
    field = [[screened_tanes_idx.pop() for _ in range(n)] for _ in range(n)]
    return field


def gen_new_tanes(tanes: list[list[int]], field: list[list[int]]) -> list[list[int]]:
    new_tanes = []
    visited = set()
    for i in range(n):
        for j in range(n):
            for di, dj in dij:
                if i + di < 0 or j + dj < 0 or n <= i + di or n <= j + dj:
                    continue
                idx1 = field[i][j]
                idx2 = field[i + di][j + dj]
                pair = (idx1, idx2) if idx1 < idx2 else (idx2, idx1)
                if pair in visited:
                    continue
                visited.add(pair)

                new_tane = [
                    random.choice([tanes[idx1][k], tanes[idx2][k]]) for k in range(m)
                ]
                new_tanes.append(new_tane)

    return new_tanes


def main():
    for _ in range(1):
        init_tanes = [list(map(int, input().split())) for _ in range(n_x)]
        start_time = time.time()
        time_limit = 1.98
        max_score = -1
        cnt = 0
        while time.time() - start_time < time_limit:
            cnt += 1
            tanes = init_tanes
            field = None
            for i in range(t):
                sc_idx = get_screened_tanes_idx()
                field = gen_field(sc_idx)
                tanes = gen_new_tanes(tanes, field)
                score = calc_score(tanes)
                if i == 0:
                    field_0 = field
            if score > max_score:
                max_score = score
                tanes = tanes
                max_field = field_0
        print(max_score)
        # for i in range(n):
        #     print(*max_field[i])


if __name__ == "__main__":
    main()
