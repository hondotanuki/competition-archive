import random
import time
import copy
from scipy.stats import zscore
from collections import deque
from math import exp

# input
_ = map(int, input().split())

# Constants
N = 6
M = 15
T = 10
NX = 60
DIJ = [(0, 1), (0, -1), (1, 0), (-1, 0)]
START_TEMPERATURE = 50
END_TEMPERATURE = 20
TIME_LIMIT = 1.99 / T
CORNERS = {(0, 0), (5, 0), (0, 5), (5, 5)}
EDGES = {
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (1, 5),
    (2, 5),
    (3, 5),
    (4, 5),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
}
CORNERS_LI = list(CORNERS)
EDGES_LI = list(EDGES)


def calc_score(tanes: list[list[int]]) -> int:
    """問題文記載のスコア算出"""
    assert len(tanes) == NX, f"len: {len(tanes)}"
    return max(sum(tane) for tane in tanes)


def generate_new_tanes(
    tanes: list[list[int]], field: list[list[int]]
) -> list[list[int]]:
    """新しい種をランダムに生成する"""
    new_tanes = []
    visited = set()
    for i in range(N):
        for j in range(N):
            for di, dj in DIJ:
                if i + di < 0 or j + dj < 0 or N <= i + di or N <= j + dj:
                    continue
                idx1 = field[i][j]
                idx2 = field[i + di][j + dj]
                pair = (idx1, idx2) if idx1 < idx2 else (idx2, idx1)
                if pair in visited:
                    continue
                visited.add(pair)

                new_tane = [
                    random.choice([tanes[idx1][k], tanes[idx2][k]]) for k in range(M)
                ]
                new_tanes.append(new_tane)

    return new_tanes


def swap_field_elements(field: list[list[int]]):
    """角と辺以外の要素をランダムに入れ替える"""
    swap = []
    q = random.randint(0, 2)
    if q == 0:
        while len(swap) < 2:
            i = random.randint(0, N - 1)
            j = random.randint(0, N - 1)
            if (i, j) in EDGES or (i, j) in CORNERS:
                continue
            swap.append((i, j))
    elif q == 1:
        swap = random.sample(EDGES_LI, 2)
    elif q == 2:
        swap = random.sample(CORNERS_LI, 2)

    (i1, j1), (i2, j2) = swap
    swapped_field = copy.deepcopy(field)
    tmp = swapped_field[i1][j1]
    swapped_field[i1][j1] = swapped_field[i2][j2]
    swapped_field[i2][j2] = tmp

    return swapped_field


def get_zscore_sorted_idx(tanes: list[list[int]]) -> list[int]:
    """標準得点に基づいて種をソートする"""
    vec_j = [[] for _ in range(M)]
    for i in range(NX):
        for j in range(M):
            vec_j[j].append(tanes[i][j])
    zscores = []
    for j in range(M):
        zscores.append([z**3 if z > 0 else z for z in zscore(vec_j[j])])
    tot_zscore = [0 for _ in range(NX)]

    for j in range(M):
        for i in range(NX):
            tot_zscore[i] += zscores[j][i]
    z_sorted_idx = deque(sorted(range(len(tot_zscore)), key=lambda k: tot_zscore[k]))
    return z_sorted_idx


def create_field(z_sorted_idx: list[int]) -> list[list[int]]:
    """辺、角という順で評価値の低い種を植える"""
    field = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if (i, j) in CORNERS and (i, j) in EDGES:
                continue
            field[i][j] = z_sorted_idx.pop()
    for edge in EDGES:
        i, j = edge
        field[i][j] = z_sorted_idx.pop()

    for corner in CORNERS:
        i, j = corner
        field[i][j] = z_sorted_idx.pop()

    return field


def process_local_input(
    tanes: list[list[int]], field: list[list[int]]
) -> list[list[int]]:
    """ビジュアライザ用の入力を読みこむ"""
    u = [input().split() for _ in range(N)]
    v = [input().split() for _ in range(N - 1)]
    res = []
    for i in range(N):
        for j in range(N):
            tane1, tane2 = [], []
            if j + 1 < N:
                for k in range(M):
                    if u[i][j][k] == "0":
                        tane1.append(tanes[field[i][j]][k])
                    elif u[i][j][k] == "1":
                        tane1.append(tanes[field[i][j + 1]][k])
            if i + 1 < N:
                for k in range(M):
                    if v[i][j][k] == "0":
                        tane2.append(tanes[field[i][j]][k])
                    elif v[i][j][k] == "1":
                        tane2.append(tanes[field[i + 1][j]][k])
            if tane1:
                res.append(tane1)
            if tane2:
                res.append(tane2)
    return res


def main():
    tanes, max_field = None, None
    for i in range(T):
        if i == 0:
            tanes = [list(map(int, input().split())) for _ in range(NX)]
        else:
            tanes = process_local_input(tanes, max_field)
        start_time = time.time()
        max_score = calc_score(tanes)
        z_sorted_idx = get_zscore_sorted_idx(tanes)
        max_field = create_field(z_sorted_idx)
        while time.time() - start_time < TIME_LIMIT:
            swapped_field = swap_field_elements(max_field)
            new_tanes = generate_new_tanes(tanes, swapped_field)
            new_score = calc_score(new_tanes)
            now_time = time.time()
            temp = (
                START_TEMPERATURE
                + (END_TEMPERATURE - START_TEMPERATURE)
                * (now_time - start_time)
                / TIME_LIMIT
            )
            delta_score = max_score - new_score
            if exp(delta_score / temp) > random.uniform(0, 1):
                max_score = new_score
                max_field = swapped_field

        for i in range(N):
            print(*max_field[i])

        with open("./out/out.txt", mode="a") as f:
            for i in range(N):
                print(*max_field[i], file=f)


if __name__ == "__main__":
    main()
