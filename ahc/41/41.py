from collections import defaultdict, deque


N, M, H = map(int, input().split())
A = list(map(int, input().split()))
tree = defaultdict(set)
for _ in range(M):
    u, v = map(int, input().split())
    tree[u].add(v)
    tree[v].add(u)

for _ in range(N):
    x, y = map(int, input().split())
ans = [-1 for _ in range(N)]
visited = set()


def bfs(u):
    ans[u] = -1
    rm_edges = []

    que = deque([u])
    dist = [-1 for _ in range(N)]
    visited.add(u)
    dist[u] = 0
    while que:
        pos = que.popleft()
        for to in tree[pos]:
            if dist[to] != -1 or to in visited:
                continue
            dist[to] = dist[pos] + 1
            if dist[pos] < H:
                ans[to] = pos
                visited.add(to)
            if dist[pos] == H:
                rm_edges.append((pos, to))

            que.append(to)
    return rm_edges


for i in range(N):
    if i in visited:
        continue
    rm_edges = bfs(i)
    if not rm_edges:
        continue
    for rm_edge in rm_edges:
        ru, rv = rm_edge
        tree[ru].remove(rv)
        tree[rv].remove(ru)

print(*ans)
