# 答えから幅と高さを概算
# def calc_score(solution: list, parts: list, direction: str):
#     if direction == "U":
#         widths = [0 for _ in range(len(parts))]
#         heigths = [0 for _ in range(max(parts))]
#     elif direction == "L":
#         widths = [0 for _ in range(max(parts))]
#         heigths = [0 for _ in range(len(parts))]

#     pre_step, cur_step = 0, 0
#     for i in range(len(parts)):
#         if direction == "U":
#             cur_step += parts[i]
#             for j, sol in enumerate(solution[pre_step:cur_step]):
#                 if (j == 0 and sol[-1] == -1) or (j != 0 and sol[-1] != -1):
#                     widths[i] += max(rects[sol[0]])
#                     heigths[j] += min(rects[sol[0]])
#                 elif j == 0 and sol[-1] != -1:
#                     widths[i - 1] += max(rects[sol[0]])
#                     heigths[j] += min(rects[sol[0]])
#                 elif j != 0 and sol[-1] == -1:
#                     widths[i + 1] += max(rects[sol[0]])
#                     heigths[0] += min(rects[sol[0]])
#             pre_step += parts[i]
#         elif direction == "L":
#             cur_step += parts[i]
#             for j, sol in enumerate(solution[pre_step:cur_step]):
#                 if (j == 0 and sol[-1] == -1) or (j != 0 and sol[-1] != -1):
#                     widths[j] += max(rects[sol[0]])
#                     heigths[i] += min(rects[sol[0]])
#                 elif j == 0 and sol[-1] != -1:
#                     widths[j] += max(rects[sol[0]])
#                     heigths[i - 1] += min(rects[sol[0]])
#                 elif j != 0 and sol[-1] == -1:
#                     widths[0] += max(rects[sol[0]])
#                     heigths[i + 1] += min(rects[sol[0]])
#             pre_step += parts[i]
#     return max(widths) + max(heigths)
