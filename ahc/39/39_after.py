import random
import time
from sortedcontainers import SortedList
import matplotlib.pyplot as plt


N = int(input())
DIV = 20
sabas = [tuple(map(int, input().split())) for _ in range(N)]
iwashis = [tuple(map(int, input().split())) for _ in range(N)]
RECT_TIME_LIM = 4


def gen_rect():
    while True:
        x, y = random.randint(0, 10**5), random.randint(0, 10**5)
        width, height = random.randint(1000, 10**4), random.randint(1000, 10**4)
        if x - width >= 0 and y - height >= 0:
            return [(x, y), (x, y - height), (x - width, y - height), (x - width, y)]


def is_point_inside_polygon(rec_min_max, x, y):
    maxx, minx, maxy, miny = rec_min_max
    return minx <= x <= maxx and miny <= y <= maxy


def calc_score(rect: list):
    score = 0
    rec_min_max = get_rect_min_max(rect)
    for saba in sabas:
        if is_point_inside_polygon(rec_min_max, saba[0], saba[1]):
            score += 1
    for iwashi in iwashis:
        if is_point_inside_polygon(rec_min_max, iwashi[0], iwashi[1]):
            score -= 1
    return score


def get_rect_min_max(rect):
    maxx, minx = -1, float("inf")
    maxy, miny = -1, float("inf")
    for x, y in rect:
        maxx = max(maxx, x)
        minx = min(minx, x)
        maxy = max(maxy, y)
        miny = min(miny, y)
    return (maxx, minx, maxy, miny)


def is_overlapping(rect1, rect2):
    """
    2つの長方形が重ならないかを判定する。
    rect1, rect2: 各長方形の4頂点 [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]
    """
    # rect1 の境界
    x1_max, x1_min, y1_max, y1_min = get_rect_min_max(rect1)
    x2_max, x2_min, y2_max, y2_min = get_rect_min_max(rect2)

    # 重ならない条件
    if x1_max <= x2_min or x2_max <= x1_min or y1_max <= y2_min or y2_max <= y1_min:
        return 0  # 重ならない
    return 1  # 重なる


def get_selected_rects(recs: SortedList):
    selected_rects = []
    rec_min_maxes = []
    while recs:
        rect = recs.pop()[1]
        overlap = 0
        for sc_rect in selected_rects:
            if is_overlapping(rect, sc_rect):
                overlap = 1
                break
        if not overlap:
            selected_rects.append(rect)
            rec_min_maxes.append(get_rect_min_max(rect))
    return selected_rects


def divide_rectangle(N):
    # 頂点座標を取得
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = (
        (0, 0),
        (10**5, 0),
        (10**5, 10**5),
        (0, 10**5),
    )

    # 左上と右下の座標を特定
    top_left_x = min(x1, x2, x3, x4)
    top_left_y = max(y1, y2, y3, y4)
    bottom_right_x = max(x1, x2, x3, x4)
    bottom_right_y = min(y1, y2, y3, y4)

    # x, y方向の分割幅を計算
    x_step = (bottom_right_x - top_left_x) / N
    y_step = (top_left_y - bottom_right_y) / N

    # 分割後の各小長方形の4頂点を格納
    grid, s_grid = [], []
    for i in range(N):
        row, s_row = [], []
        for j in range(N):
            # 各小長方形の4頂点を計算
            small_top_left = (top_left_x + j * x_step, top_left_y - i * y_step)
            small_top_right = (top_left_x + (j + 1) * x_step, top_left_y - i * y_step)
            small_bottom_left = (top_left_x + j * x_step, top_left_y - (i + 1) * y_step)
            small_bottom_right = (
                top_left_x + (j + 1) * x_step,
                top_left_y - (i + 1) * y_step,
            )

            # 頂点をリストに追加
            row.append(
                (small_bottom_left, small_bottom_right, small_top_right, small_top_left)
            )
            s_row.append(
                calc_score(
                    (
                        small_bottom_left,
                        small_bottom_right,
                        small_top_right,
                        small_top_left,
                    )
                )
            )
        grid.append(row)
        s_grid.append(s_row)
    return grid, s_grid


def plot_quadrilaterals(points_list):
    """
    複数の四角形を描画する。
    :param points_list: 各四角形の4点のリスト [[(x1, y1), (x2, y2), (x3, y3), (x4, y4)], ...]
    """
    for points in points_list:
        x, y = zip(*points)
        x = list(x) + [x[0]]
        y = list(y) + [y[0]]
        plt.plot(x, y, marker="o")

    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def plot_scatter(points):
    if not points:
        print("点のリストが空です。")
        return
    x_coords, y_coords = zip(*points)  # x座標とy座標を分ける
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, marker="o", color="blue")
    plt.title("Scatter Plot of Points")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.show()


def main():
    grid, s_grid = divide_rectangle(DIV)
    # print(grid[0])
    for s in s_grid:
        print(s)
    # start_time = time.time()
    # rects = SortedList([])
    # while time.time() - start_time < RECT_TIME_LIM:
    #     rect = gen_rect()
    #     score = calc_score(rect)
    #     rects.add((score, rect))
    #     if len(rects) > 300:
    #         rects.pop(0)

    # sc_rects = get_selected_rects(rects)

    # 重ならない範囲で長方形を描いた
    # print(sc_rects)
    # rects = [rect[1] for rect in rects]
    # plot_quadrilaterals(sc_rects)
    # TODO: 描いた長方形をつなげるところから
    # パスを適当に


if __name__ == "__main__":
    main()
