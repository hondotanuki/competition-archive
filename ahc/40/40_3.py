import copy
from itertools import product
import random
from sortedcontainers import SortedList

# input
N, T, sig = map(int, input().split())
rects = [list(map(int, input().split())) for _ in range(N)]

# 分割数を探索する範囲
DIV_MIN = 1
DIV_MAX = 20
INIT_NUM = 6
FINAL_SUBMIT_NUM = 6


# NOTE: 簡単のためdirectionをLのみUのみで固定している
def draw_true_rect(draw):
    """真の四角形を取得し、変更を反映"""
    idx_list = [i for i in range(N)]
    samples = random.sample(idx_list, draw)

    for sample in samples:
        print(1)
        print(sample, 0, "U", -1)
        w, h = map(int, input().split())
        rects[sample] = [w, h]


def get_parts(div: int) -> list:
    """div分割するときの各列・行の要素数"""
    q, r = divmod(N, div)
    return [q + 1] * r + [q] * (div - r)


def gen_solution(parts: list, direction: str) -> list:
    """L, Uを固定して0~Nまで積んでいき、solutionを作成"""
    idx = 0
    solution = []
    for part in parts:
        parent_idx = -1
        for _ in range(part):
            wd, hd = rects[idx]
            rot = int(hd > wd)
            solution.append([idx, rot, direction, parent_idx])
            parent_idx = idx
            idx += 1
    solution.sort()
    return solution


def create_graph(div: int, parts: list[int], direction: str):
    """どこに四角を置いたかのグラフを作成"""
    max_parts = max(parts)
    if direction == "U":
        graph = [[-1 for _ in range(max_parts)] for _ in range(div)]
        idx = 0
        for i in range(div):
            for j in range(parts[i]):
                graph[i][j] = idx
                idx += 1
                if idx == N:
                    return graph
    else:
        graph = [[-1 for _ in range(div)] for _ in range(max_parts)]
        idx = 0
        for j in range(div):
            for i in range(parts[j]):
                graph[i][j] = idx
                idx += 1
                if idx == N:
                    return graph
    return graph


def calc_score(graph):
    """グラフからスコアを算出"""
    widths = [0 for _ in range(len(graph[0]))]
    heigths = [0 for _ in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == -1:
                continue
            widths[j] += max(rects[graph[i][j]])
            heigths[i] += min(rects[graph[i][j]])
    return max(widths) + max(heigths)


def create_init_stats():
    """スコアでソートされたステータス"""
    init_stats = SortedList([])
    for direction in ["U", "L"]:
        for div in range(DIV_MIN, DIV_MAX):
            parts = get_parts(div)
            assert sum(parts) == N
            cur_g = create_graph(div, parts, direction)
            cur_sol = gen_solution(parts, direction)
            cur_score = calc_score(cur_g)
            init_stats.add((cur_score, cur_g, parts, cur_sol))
            if len(init_stats) > INIT_NUM:
                # 上位INIT_GEN_LIM個のみ使用
                init_stats.pop()
    return init_stats


def swap_graph_and_solution(prod, graph, parts, solution):
    step = 0
    for i in range(len(prod)):
        step += parts[i]

        if prod[i] == 0:
            continue
        if solution[0][2] == "U":
            graph[i][-1], graph[i + 1][0] = graph[i + 1][0], graph[i][-1]
        else:
            graph[-1][i], graph[0][i + 1] = graph[0][i + 1], graph[-1][i]

        solution[step - 1][-1], solution[step][-1], solution[step + 1][-1] = (
            -1,
            solution[step - 1][-1],
            solution[step - 1][0],
        )


def reset_graph_and_solution(prod, graph, parts, solution):
    step = 0
    for i in range(len(prod)):
        step += parts[i]
        if prod[i] == 0:
            continue
        if solution[0][2] == "U":
            graph[i][-1], graph[i + 1][0] = graph[i + 1][0], graph[i][-1]
        else:
            graph[-1][i], graph[0][i + 1] = graph[0][i + 1], graph[-1][i]
        solution[step - 1][-1], solution[step][-1], solution[step + 1][-1] = (
            solution[step - 1][0] - 1,
            -1,
            solution[step + 1][0] - 1,
        )


# 初期解作成に6回、最終回答に6回づつ提出する
# それ以外を四角w, h確定に充てる
draw = min(T - FINAL_SUBMIT_NUM, N)
draw_true_rect(draw)
T -= draw

# 初期解作成
init_stats = create_init_stats()
assert len(init_stats) == INIT_NUM

ans_list = []
dirs = ["U", "L"]
for init_stat in init_stats:
    score, graph, parts, solution = init_stat
    best_ans = copy.deepcopy(solution)
    best_score = score
    for prod in product([0, 1], repeat=(len(parts)) - 1):
        swap_graph_and_solution(prod, graph, parts, solution)
        cur_score = calc_score(graph)
        if best_score > cur_score:
            best_ans = copy.deepcopy(solution)
            best_score = cur_score
        reset_graph_and_solution(prod, graph, parts, solution)
    ans_list.append(best_ans)


for ans in ans_list:
    print(len(ans))
    for a in ans:
        print(*a)
    w, h = map(int, input().split())
    T -= 1

while T > 0:
    print(N)
    for a in ans:
        print(*a)
    w, h = map(int, input().split())
    T -= 1
