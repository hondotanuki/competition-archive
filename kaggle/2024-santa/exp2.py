import numpy as np
import matplotlib.pyplot as plt
import random


class A:
    def get_perplexity():
        pass


scorer = A
neighbor_range = 5
scores = None


def quadratic_fit_and_residuals(x_values, y_values):
    """
    x_values: フィッティング対象のxのリスト (実数)
    y_values: フィッティング対象のyのリスト (実数)

    戻り値:
    1. フィットに用いた2次多項式 p(x) (numpy.poly1d)
    2. 残差を大きい順に並べたリスト ( [(インデックス, 残差), ...] )
    """

    x = np.array(x_values)
    y = np.array(y_values)

    # 2次多項式でフィッティング
    coeffs = np.polyfit(x, y, 2)
    p = np.poly1d(coeffs)

    # 近似値を計算
    y_est = p(x)

    # 残差(実測値 - 推定値)の計算
    residuals = y - y_est

    # 残差を大きい順にソート (インデックスも保持)
    residuals_with_index = sorted(
        [(i, r) for i, r in enumerate(residuals)], key=lambda tup: tup[1], reverse=True
    )

    # 可視化
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, label="Original data", color="blue")
    x_fit = np.linspace(min(x), max(x), 200)
    y_fit = p(x_fit)
    plt.plot(x_fit, y_fit, label="Fitted quadratic curve", color="red")
    plt.title("Quadratic Fitting")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()

    return p, residuals_with_index


def swap_high_residual_ranges(neighbor, k):
    """
    上位kの残差を持つインデックスの中からランダムに2件を取り出し、
    それをもとにランダムな範囲を入れ替える
    """
    # i, j = random.sample(range(k), 2)
    # a_start, _ = self.resid[i]
    # b_start, _ = self.resid[j]
    a_start = 3
    b_start = 20
    n = len(neighbor)
    if b_start < a_start:
        a_start, b_start = b_start, a_start

    while True:
        a_end = random.randrange(a_start + 1, min(a_start + neighbor_range, n + 1))
        b_end = random.randrange(b_start + 1, min(b_start + neighbor_range, n + 1))
        # 重ならないようにチェック
        if a_end <= b_start or b_end <= a_start:
            break

    part_before_A = neighbor[:a_start]
    A_part = neighbor[a_start:a_end]
    middle = neighbor[a_end:b_start]
    B_part = neighbor[b_start:b_end]
    part_after_B = neighbor[b_end:]

    neighbor = part_before_A + B_part + middle + A_part + part_after_B
    return neighbor


id_ = 5
# df = pd.read_csv("aaa")
solution = [chr(i) for i in range(65, 91)]
print(solution)
print(swap_high_residual_ranges(solution, 2))
# cur_solution = []
# scores = []
# for i in range(n):
#     cur_solution += solution[i]
#     text = " ".join(cur_solution)
#     score = scorer.get_perplexity(text)
#     scores.append(score)

# y_data = scores
# x_data = [i for i in range(1, len(scores) + 1)]

# # 関数実行
# fitted_poly, resid = quadratic_fit_and_residuals(x_data, y_data)

# # フィットされた2次多項式を表示
# print("Fitted polynomial:\n", fitted_poly)

# # 残差が大きい順のリストを表示
# print("Sorted residuals (index, residual):")
# for idx, res in resid:
#     print(f"Index: {idx}, Residual: {res:.4f}")
