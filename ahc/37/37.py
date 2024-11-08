import sys
from sortedcontainers import SortedList


def calc_score(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1]) - (u[0] + u[1] + v[0] + v[1])


n = int(sys.stdin.readline())
nodes = SortedList([tuple(map(int, sys.stdin.readline().split())) for _ in range(n)])
ans_rev = []
while len(nodes) > 1:
    min_score = float("inf")
    min_u = None
    min_v = None
    n = len(nodes)
    for i in range(n):
        for j in range(i + 1, n):
            score = calc_score(nodes[i], nodes[j])
            if score < min_score:
                min_score = score
                min_u, min_v = nodes[i], nodes[j]

    aux_x = min_u[0] if min_u[0] < min_v[0] else min_v[0]
    aux_y = min_u[1] if min_u[1] < min_v[1] else min_v[1]
    aux_node = (aux_x, aux_y)
    nodes.discard(min_u)
    nodes.discard(min_v)
    nodes.add(aux_node)
    if min_u != aux_node:
        ans_rev.append([aux_node[0], aux_node[1], min_u[0], min_u[1]])
    if min_v != aux_node:
        ans_rev.append([aux_node[0], aux_node[1], min_v[0], min_v[1]])

if (x := nodes[-1][0], y := nodes[-1][1]) != (0, 0):
    ans_rev.append([0, 0, x, y])

m = len(ans_rev)
print(m)
for i in range(1, m + 1):
    print(*ans_rev[m - i])
