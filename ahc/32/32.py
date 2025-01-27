from sortedcontainers import SortedList
import copy

BEAM_WIDTH = 2
MOD = 998244353

N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
stamps = [[list(map(int, input().split())) for _ in range(3)] for _ in range(M)]


def calc_score():
    score = 0
    for i in range(N):
        for j in range(N):
            score += graph[i][j] % MOD
    return score


def add_value(m, p, q):
    for i in range(3):
        for j in range(3):
            graph[p + i][q + j] += stamps[m][i][j]


def restore_value(m, p, q):
    for i in range(3):
        for j in range(3):
            graph[p + i][q + j] -= stamps[m][i][j]


solutions = SortedList([[0, []]])
for _ in range(K):
    candidates = SortedList()
    for score_sol in solutions:
        current_score, cur_sol = score_sol
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    new_solution = cur_sol + [(m, i, j)]
                    n = len(new_solution)
                    for cs in range(n):
                        cm, ci, cj = new_solution[cs]
                        add_value(cm, ci, cj)
                    score = calc_score()
                    for cs in range(n):
                        cm, ci, cj = new_solution[cs]
                        restore_value(cm, ci, cj)
                    candidates.add([-score, new_solution])
                    if len(candidates) > BEAM_WIDTH:
                        candidates.pop()
    solutions = copy.deepcopy(candidates)

with open("ahc/32/out.txt", "w") as f:
    print(len(solutions[0][1]), file=f)
    for m, i, j in solutions[0][1]:
        print(m, i, j, file=f)
