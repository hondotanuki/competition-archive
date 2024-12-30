from sortedcontainers import SortedList

N, T, sigma = map(int, input().split())

rects = []
for i in range(N):
    turn = 0
    wd, hd = map(int, input().split())
    if wd < hd:
        wd, hd = hd, wd
        turn = 1
    rects.append((wd, hd, i, turn))
rects.sort(reverse=True)
print(rects)
ans = SortedList([])
for i in range(N // 2):
    rect = rects[i]
    if i == 0:
        ans.add((rect[2], rect[3], "L", -1))
    else:
        ans.add((rect[2], rect[3], "L", rects[i - 1][2]))

# for i in range(N // 2 if N % 2 == 0 else N // 2 + 1):
#     rect = rects[N - i - 1]
#     if i == 0:
#         ans.add((rect[2], rect[3], "L", -1))
#     else:
#         ans.add((rect[2], rect[3], "L", rects[i - 1][2]))

with open("out.txt", mode="w") as f:
    print(len(ans), file=f)
    for a in ans:
        print(*a, file=f)
