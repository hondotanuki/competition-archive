import sys
import heapq
import copy

input = sys.stdin.readline
MOD = 998244353
BEAM_WIDTH = 2

N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
stamps = [[list(map(int, input().split())) for _ in range(3)] for _ in range(M)]

# 各スタンプの合計値を前計算
stamp_sums = []
for m in range(M):
    s = 0
    for x in range(3):
        for y in range(3):
            s += stamps[m][x][y]
    stamp_sums.append(s % MOD)


def add_value(m, px, py, mat):
    for i in range(3):
        for j in range(3):
            mat[px + i][py + j] = (mat[px + i][py + j] + stamps[m][i][j]) % MOD


def restore_value(m, px, py, mat):
    for i in range(3):
        for j in range(3):
            mat[px + i][py + j] = (mat[px + i][py + j] - stamps[m][i][j]) % MOD


def compute_score(mat):
    total = 0
    for row in mat:
        total += sum(row)
    return total % MOD


# 初期状態のスコア計算
init_score = compute_score(graph)

# ビームに入れる (score, 行列, [スタンプの押し方の履歴])
# heapq で最大スコアを取り出したいので -score を優先度にする
solutions = [(-init_score, init_score, [row[:] for row in graph], [])]

for _ in range(K):
    candidates = []
    # ビーム幅分だけループ (最大で BEAM_WIDTH 個)
    for _ in range(len(solutions)):
        neg_score_cur, score_cur, mat_cur, moves_cur = heapq.heappop(solutions)
        score_cur %= MOD

        # ここで全スタンプ × 全配置 を試す
        for m in range(M):
            # (正味マイナスになりそうなスタンプはスキップしたければ条件を付ける)
            # 例: if stamp_sums[m] <= 0: continue

            for i in range(N - 2):
                for j in range(N - 2):
                    # 新しい行列をコピー
                    new_mat = [row[:] for row in mat_cur]

                    # スタンプ適用
                    add_value(m, i, j, new_mat)

                    # スコア更新 (O(1))
                    new_score = (score_cur + stamp_sums[m]) % MOD

                    # 新しい move リスト
                    new_moves = moves_cur + [(m, i, j)]

                    # 候補に追加 (heapq ではタプルの先頭要素で優先度比較)
                    heapq.heappush(
                        candidates, (-new_score, new_score, new_mat, new_moves)
                    )

    # candidatesの中から上位 BEAM_WIDTH 個だけを次の solutions にする
    solutions = []
    for _ in range(min(BEAM_WIDTH, len(candidates))):
        solutions.append(heapq.heappop(candidates))

# 最終的に一番スコアの高い解 (heap の先頭) を出力
best_neg, best_score, best_mat, best_moves = solutions[0]

with open("ahc/32/out.txt", "w") as f:
    print(len(best_moves), file=f)
    for m, i, j in best_moves:
        print(m, i, j, file=f)
