import random
import time

N = int(input())
sabas = [tuple(map(int, input().split())) for _ in range(N)]
iwashis = [tuple(map(int, input().split())) for _ in range(N)]
TIME_LIMIT = 1.98


def gen_rec():
    while True:
        x, y = random.randint(0, 10**5), random.randint(0, 10**5)
        width, height = random.randint(500, 10**5), random.randint(500, 10**5)
        if x - width >= 0 and y - height >= 0:
            return [(x, y), (x, y - height), (x - width, y - height), (x - width, y)]


def is_point_inside_polygon(maxx, minx, maxy, miny, x, y):
    if minx <= x <= maxx and miny <= y <= maxy:
        return 1
    else:
        return 0


def main():
    start_time = time.time()
    max_cnt = -1
    max_rec = None
    while time.time() - start_time < TIME_LIMIT:
        cnt = 0
        rec = gen_rec()
        maxx, minx = -1, float("inf")
        maxy, miny = -1, float("inf")
        for x, y in rec:
            maxx = max(maxx, x)
            minx = max(minx, x)
            maxy = max(maxy, y)
            miny = max(miny, y)
        for saba in sabas:
            if is_point_inside_polygon(maxx, minx, maxy, miny, saba[0], saba[1]):
                cnt += 1
        for iwashi in iwashis:
            if is_point_inside_polygon(maxx, minx, maxy, miny, iwashi[0], iwashi[1]):
                cnt -= 1
        if cnt > max_cnt:
            max_cnt = cnt
            max_rec = rec

    print(len(max_rec))
    for r in max_rec:
        print(*r)


if __name__ == "__main__":
    main()
