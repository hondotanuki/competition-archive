import random


def swap_two_random_ranges(solution):
    n = len(solution)

    while True:
        a_start = random.randrange(n)
        a_end = random.randrange(a_start + 1, n + 1)  # a_start < a_end

        b_start = random.randrange(n)
        b_end = random.randrange(b_start + 1, n + 1)  # b_start < b_end

        # 重ならないようにチェック
        if a_end <= b_start or b_end <= a_start:
            break

    if b_start < a_start:
        a_start, a_end, b_start, b_end = b_start, b_end, a_start, a_end

    # ここまでくれば必ず a_start < b_start
    part_before_A = solution[:a_start]
    A_part = solution[a_start:a_end]
    middle = solution[a_end:b_start]
    B_part = solution[b_start:b_end]
    part_after_B = solution[b_end:]

    neighbor = part_before_A + B_part + middle + A_part + part_after_B
    return neighbor


def swap_and_shuffle_two_random_ranges(solution):
    """ランダムな二つの範囲内の要素を抽出・シャッフルし入れ替え"""

    n = len(solution)
    while True:
        start1 = random.randrange(n)
        end1 = random.randrange(start1 + 1, n + 1)
        start2 = random.randrange(n)
        end2 = random.randrange(start2 + 1, n + 1)
        (front_start, front_end), (back_start, back_end) = sorted(
            [(start1, end1), (start2, end2)], key=lambda x: x[0]
        )

        # 重ならないならループを抜ける
        if front_end <= back_start:
            break
    print((front_start, front_end), (back_start, back_end))
    front_part = solution[front_start:front_end]
    back_part = solution[back_start:back_end]

    # 範囲内の要素をランダムに並び替え
    random.shuffle(front_part)
    random.shuffle(back_part)

    # front と back を入れ替え
    neighbor = (
        solution[:front_start]
        + back_part
        + solution[front_end:back_start]
        + front_part
        + solution[back_end:]
    )

    return neighbor


# 動作確認
data = list(range(10))
print("元のリスト:", data)

swapped_data = swap_two_random_ranges(data)
print("入れ替え後のリスト:", swapped_data)
print(data)
swapped_data = swap_and_shuffle_two_random_ranges(data)
print("入れ替え後のリスト:", swapped_data)
print(data)
