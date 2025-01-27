from itertools import combinations as comb


def shift_range_forward(solution, i, j):
    return solution[:i] + [solution[j]] + solution[i:j] + solution[j + 1 :]


def shift_range_backward(solution, i, j):
    return solution[:i] + solution[i + 1 : j + 1] + [solution[i]] + solution[j + 1 :]


def shift_random_ranges(solution: list[str], min_range: int):
    solutions = []
    n = len(solution)
    for i, j, k, l in comb(range(n), 4):
        if (j - i) < min_range or (l - k) < min_range:  # 短すぎる区間はスキップ
            continue
        sol_f = shift_range_forward(solution, i, j)
        sol_b = shift_range_backward(solution, i, j)

        sol_ff = shift_range_forward(sol_f, k, l)
        sol_bf = shift_range_forward(sol_b, k, l)
        sol_bb = shift_range_backward(sol_b, k, l)
        sol_fb = shift_range_backward(sol_f, k, l)

        solutions.append(sol_ff)
        solutions.append(sol_bf)
        solutions.append(sol_bb)
        solutions.append(sol_fb)

    new_solutions = set()
    for sol in solutions:
        new_solutions.add(tuple(sol))
    return new_solutions


solution = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"] * 3
new_solutions = shift_random_ranges(solution, 2)

s = set()
for solution in new_solutions:
    s.add(len(solution))
print(s)
