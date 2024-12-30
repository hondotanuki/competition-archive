N, T, sigma = map(int, input().split())

rects = []
rects = [list(map(int, input().split())) for _ in range(N)]

for t in range(1, T + 1):
    div = t if t < N else N
    print(N)
    for i in range(N):
        rot = 0
        wd, hd = rects[i][0], rects[i][1]
        if hd > wd:
            rot = 1
        if i % (N // div) == 0:
            print(i, rot, "L", -1)
        else:
            print(i, rot, "L", i - 1)

    w, h = map(int, input().split())


# 1615: 青パフォ
