import sys
from collections import deque, defaultdict

sys.setrecursionlimit(10**7)


def bfs_farthest(start, comp, tree):
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


def build_rooted_tree(comp, tree, root):
    """親ノードの取得"""
    parent = {c: None for c in comp}
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


N, M, H = map(int, input().split())
A = list(map(int, input().split()))

tree = defaultdict(set)
for _ in range(M):
    u, v = map(int, input().split())
    tree[u].add(v)
    tree[v].add(u)

for _ in range(N):
    x, y = map(int, input().split())


all_nodes = set(range(N))
queue_comp = deque([all_nodes])
result_components = []

while queue_comp:
    comp = queue_comp.popleft()
    if not comp:
        continue

    unvisited = set(comp)
    sub_comps = []
    while unvisited:
        start = next(iter(unvisited))
        visited_temp = set([start])
        q = deque([start])
        while q:
            cur = q.popleft()
            for nxt in tree[cur]:
                if nxt in unvisited and nxt not in visited_temp:
                    visited_temp.add(nxt)
                    q.append(nxt)
        sub_comps.append(visited_temp)
        unvisited -= visited_temp

    for sub in sub_comps:
        if len(sub) <= 1:
            result_components.append(sub)
            continue
        any_node = next(iter(sub))
        u, _, _, _ = bfs_farthest(any_node, sub, tree)
        v, diameter, parent_v, dist_v = bfs_farthest(u, sub, tree)

        if diameter <= H:
            result_components.append(sub)
        else:
            path_uv = get_path(u, v, parent_v)
            d = len(path_uv) - 1
            mid_edge_idx = d // 2
            a = path_uv[mid_edge_idx]
            b = path_uv[mid_edge_idx + 1]

            tree[a].remove(b)
            tree[b].remove(a)
            visited_a = set([a])
            qa = deque([a])
            while qa:
                cur = qa.popleft()
                for nxt in tree[cur]:
                    if nxt in sub and nxt not in visited_a:
                        visited_a.add(nxt)
                        qa.append(nxt)
            comp_a = visited_a
            comp_b = sub - comp_a
            queue_comp.append(comp_a)
            queue_comp.append(comp_b)

ans = [None] * N

for comp in result_components:
    if len(comp) == 1:
        c = next(iter(comp))
        ans[c] = -1
        continue
    any_node = next(iter(comp))
    u, _, _, _ = bfs_farthest(any_node, comp, tree)
    v, diameter, parent_v, dist_v = bfs_farthest(u, comp, tree)
    path_uv = get_path(u, v, parent_v)
    d = len(path_uv) - 1

    center_idx = d // 2
    root = path_uv[center_idx]
    parent_map = build_rooted_tree(comp, tree, root)
    for node in comp:
        ans[node] = parent_map[node]

print(*ans)
