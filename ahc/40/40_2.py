N, T, sigma = map(int, input().split())

rects = [list(map(int, input().split())) for _ in range(N)]

ln = T // 2
un = T - T // 2

for t in range(2, 2 + ln):
    div = t if t < N else N
    print(N)
    for i in range(N):
        rot = 0
        wd, hd = rects[i][0], rects[i][1]
        if hd > wd:
            rot = 1
        if i % (N // div + 1) == 0:
            print(i, rot, "L", -1)
        else:
            print(i, rot, "L", i - 1)
    w, h = map(int, input().split())

for t in range(2, 2 + un):
    div = t if t < N else N
    print(N)
    for i in range(N):
        rot = 0
        wd, hd = rects[i][0], rects[i][1]
        if hd > wd:
            rot = 1
        if i % (N // div + 1) == 0:
            print(i, rot, "U", -1)
        else:
            print(i, rot, "U", i - 1)
    w, h = map(int, input().split())
