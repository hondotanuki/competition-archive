from itertools import permutations


def two_ranges_permutation(lst, range1, range2):
    """
    lst      : 処理対象となる元リスト
    range1   : (start1, end1) のタプル (end1は非含む)
    range2   : (start2, end2) のタプル (end2は非含む)

    それぞれの部分リストの全順列を生成し、
    毎回元リストに埋め込んだリストを返すジェネレータを返す。
    """

    start1, end1 = range1
    start2, end2 = range2

    # もし2つの範囲が重なる場合はエラーにするなどのチェック
    if not (end1 <= start2 or end2 <= start1):
        raise ValueError(
            "指定した範囲が重なっています。range1={}, range2={}".format(range1, range2)
        )

    sub1 = lst[start1:end1]  # 範囲1の部分リスト
    sub2 = lst[start2:end2]  # 範囲2の部分リスト

    # 部分リストの「重複しない全順列」をそれぞれセット化
    unique_perm_sub1 = set(permutations(sub1))
    unique_perm_sub2 = set(permutations(sub2))

    # 2つの順列集合のデカルト積を取りながら、元リストに埋め込む
    for perm1 in unique_perm_sub1:
        for perm2 in unique_perm_sub2:
            new_list = (
                lst[:start1] + list(perm1) + lst[end1:start2] + list(perm2) + lst[end2:]
            )
            yield new_list


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 例:
    #   range1 = (2, 5) => インデックス2〜4 (要素[3,4,5])
    #   range2 = (7, 9) => インデックス7〜8 (要素[8,9])
    #   ※end1 <= start2 の順で範囲が重ならないように指定

    range1 = (2, 5)
    range2 = (7, 9)

    # すべてのパターンを列挙 (全探索)
    for i, perm_list in enumerate(two_ranges_permutation(data, range1, range2)):
        print(f"パターン {i:3d}: {perm_list}")

    # リストとしてすべてを受け取りたいなら、以下のようにもできる
    # all_patterns = list(all_permutations_for_two_ranges(data, range1, range2))
    # print("総パターン数:", len(all_patterns))
