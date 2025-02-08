N = int(input())
G = [list(input()) for _ in range(N)]
oni = 2 * N
fuku = 2 * N


def minus_fuku_or_oni(element):
    global oni, fuku
    if element == "o":
        fuku -= 1
    elif element == "x":
        oni -= 1


def calc_official_score(T):
    global oni, fuku
    assert oni >= 0 and fuku >= 0, "鬼か福の値おかしい"
    if oni == 0 and fuku == 0:
        return 8 * N**2 - T
    else:
        return 4 * N**2 - N * (oni + fuku)


def move_graph(dir, idx):
    assert dir in {"L", "R", "U", "D"}, "方向ミス"
    assert 0 <= idx < N, f"{idx=} out of range"

    if dir == "L":
        minus_fuku_or_oni(G[idx][0])
        G[idx][0] = "."
        for j in range(N - 1):
            G[idx][j] = G[idx][j + 1]
        G[idx][N - 1] = "."
    elif dir == "R":
        minus_fuku_or_oni(G[idx][N - 1])
        G[idx][N - 1] = "."
        for j in range(N - 1, 0, -1):
            G[idx][j] = G[idx][j - 1]
        G[idx][0] = "."
    elif dir == "U":
        minus_fuku_or_oni(G[0][idx])
        G[0][idx] = "."
        for i in range(N - 1):
            G[i][idx] = G[i + 1][idx]
        G[N - 1][idx] = "."
    elif dir == "D":
        minus_fuku_or_oni(G[N - 1][idx])
        G[N - 1][idx] = "."
        for i in range(N - 1, 0, -1):
            G[i][idx] = G[i - 1][idx]
        G[0][idx] = "."
    return G


def calc_move_score(i, j):
    """
    4方向に対して鬼を1、福を-1としてカウント後、
    移動数で割ったスコアを返す。大きいほど良い
    """

    def _count(i, j, count):
        if G[i][j] == "o":
            count -= 1
        elif G[i][j] == "x":
            count += 1
        return count

    count_l, count_r, count_u, count_d = 0, 0, 0, 0
    for m in range(1, N):
        if 0 <= j - m:
            count_l = _count(i, j - m, count_l)
        if j + m < N:
            count_r = _count(i, j + m, count_r)
        if 0 <= i - m:
            count_u = _count(i - m, j, count_u)
        if i + m < N:
            count_d = _count(i + m, j, count_d)

    score_l = count_l / (j + 1)
    score_r = count_r / (N - j)
    score_u = count_u / (i + 1)
    score_d = count_d / (N - j)
    max_score = max(score_l, score_r, score_u, score_d)
    scores_move = {
        score_l: ("L", i, j + 1),
        score_r: ("R", i, N - j),
        score_u: ("U", j, i + 1),
        score_d: ("D", j, N - i),
    }
    return (max_score, scores_move[max_score])


def get_good_move():
    moves = []
    for i in range(N):
        for j in range(N):
            if G[i][j] == "x":
                moves.append(calc_move_score(i, j))
    moves.sort(reverse=True)
    return moves[0][1]


T = 0
ans = []
while oni > 0 and T < 4 * N**2:
    direction, idx, times = get_good_move()
    for _ in range(times):
        move_graph(direction, idx)
        ans.append((direction, idx))
        T += 1

with open("out.txt", "w") as f:
    for a in ans:
        print(*a, file=f)
