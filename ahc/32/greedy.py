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
            graph[p + i][q + j] %= MOD


def restore_value(m, p, q):
    for i in range(3):
        for j in range(3):
            graph[p + i][q + j] -= stamps[m][i][j]
            if graph[p + i][q + j] < 0:
                graph[p + i][q + j] += MOD


best_score, best_solution = -1, []
while len(best_solution) < K:
    cur_score, cur_solution = -1, None
    for m in range(M):
        for i in range(N):
            for j in range(N):
                if N <= i + 2 or N <= j + 2:
                    continue
                add_value(m, i, j)
                score = calc_score()
                restore_value(m, i, j)
                if cur_score < score:
                    cur_score = score
                    cur_solution = (m, i, j)

    if best_score < cur_score:
        best_score = cur_score
        best_solution += [cur_solution]
        print(best_solution)
        add_value(*cur_solution)
    else:
        break


with open("ahc/32/out.txt", "w") as f:
    print(len(best_solution), file=f)
    for i in range(len(best_solution)):
        m, i, j = best_solution[i]
        print(m, i, j, file=f)
