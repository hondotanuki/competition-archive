import random
from collections import deque, defaultdict
import os

# 読み込みたいディレクトリのパスを指定
directory = "ahc/41/input"

# ディレクトリ内のすべてのファイルを取得
txt_files = [file for file in os.listdir(directory) if file.endswith(".txt")]

# ファイル内容を辞書に保存
data_dict = {}

# N, M, H = map(int, input().split())
# A = list(map(int, input().split()))
# tree = defaultdict(set)
# for _ in range(M):
#     u, v = map(int, input().split())
#     tree[u].add(v)
#     tree[v].add(u)

# for _ in range(N):
#     x, y = map(int, input().split())
for t, txt_file in enumerate(txt_files):
    print()
    with open(os.path.join(directory, txt_file), "r") as file:
        lines = file.readlines()
    # 入力データのパース
    # 最初の行：N, M, H
    N, M, H = map(int, lines[0].split())

    # 2行目：リストA
    A = list(map(int, lines[1].split()))

    # 次のM行：辺情報
    tree = defaultdict(set)
    for i in range(2, 2 + M):
        u, v = map(int, lines[i].split())
        tree[u].add(v)
        tree[v].add(u)

    # 最後のN行：座標情報
    coordinates = []
    for i in range(2 + M, 2 + M + N):
        x, y = map(int, lines[i].split())

    def bfs_farthest(start, comp):
        """木の直径"""
        visited = set([start])
        dist = {start: 0}
        parent = {start: None}
        queue = deque([start])

        while queue:
            cur = queue.popleft()
            for nxt in tree[cur]:
                if nxt not in visited and nxt in comp:
                    visited.add(nxt)
                    parent[nxt] = cur
                    dist[nxt] = dist[cur] + 1
                    queue.append(nxt)

        farthest_node = max(visited, key=lambda x: dist[x])
        return farthest_node, dist[farthest_node], parent, dist

    def get_path(u, v, parent):
        """パスの取得"""
        path = []
        cur = v
        while cur is not None:
            path.append(cur)
            if cur == u:
                break
            cur = parent[cur]
        path.reverse()
        return path

    all_nodes = set(range(N))
    queue_comp = deque()
    queue_comp.append(all_nodes)

    result_components = []

    while queue_comp:
        comp = queue_comp.popleft()
        if not comp:
            continue

        start_node = next(iter(comp))

        u, _, parent_u, dist_u = bfs_farthest(start_node, comp)
        v, diameter, parent_v, dist_v = bfs_farthest(u, comp)

        if diameter <= H:
            result_components.append(comp)
            continue

        path_uv = get_path(u, v, parent_v)
        d = len(path_uv) - 1
        mid_edge_idx = d // 2
        a = path_uv[mid_edge_idx]
        b = path_uv[mid_edge_idx + 1]

        tree[a].remove(b)
        tree[b].remove(a)

        visited_a = set([a])
        queue_a = deque([a])
        while queue_a:
            cur = queue_a.popleft()
            for nxt in tree[cur]:
                if nxt not in visited_a and nxt in comp:
                    visited_a.add(nxt)
                    queue_a.append(nxt)

        comp_a = visited_a
        comp_b = comp - comp_a

        queue_comp.append(comp_a)
        queue_comp.append(comp_b)

    def build_rooted_tree(comp, tree, root):
        """親ノードの取得"""
        parent = {}
        for c in comp:
            parent[c] = None

        parent[root] = -1
        visited = set([root])
        queue = deque([root])

        while queue:
            cur = queue.popleft()
            for nxt in tree[cur]:
                if nxt in comp and nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = cur
                    queue.append(nxt)

        return parent

    comp_id = 0
    ans = [float("inf") for _ in range(N)]
    for comp in result_components:
        comp_id += 1
        comp_list = list(comp)

        root = random.choice(comp_list)
        parent_map = build_rooted_tree(comp, tree, root)

        children_map = defaultdict(list)
        for node in comp:
            p = parent_map[node]
            children_map[p].append(node)

        all_parents_sorted = sorted(children_map.keys(), key=lambda x: (x != -1, x))

        for p in all_parents_sorted:
            children = children_map[p]
            for c in children:
                ans[c] = p
    name = txt_file.split(".")[0]
    with open(f"ahc/41/output/{name}.txt", "w") as f:
        print(*ans, file=f)
