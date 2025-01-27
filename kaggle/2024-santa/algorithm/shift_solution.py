def shift_solution(solution):
    n = len(solution)
    results = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            subrange = solution[i:j]
            if len(subrange) == 1:
                continue
            shifted_subrange = [subrange[-1]] + subrange[:-1]
            new_words = solution[:i] + shifted_subrange + solution[j:]
            results.append(" ".join(new_words))
            shifted_subrange = subrange[1:] + [subrange[0]]
            new_words = solution[:i] + shifted_subrange + solution[j:]
            results.append(" ".join(new_words))
    return list(set(results))


# -------------- 実行例 --------------
if __name__ == "__main__":
    solution = ["I", "have", "a", "pen"]
    all_shifted = shift_solution(solution)
    for idx, seq in enumerate(all_shifted, 1):
        print(f"{seq}")


# サンプルデータ
# id_ = 3
# best_text = df.loc[id_, "text"]
# texts = shift_solution(best_text.split())
# best_score = scorer.get_perplexity(df.loc[id_, "text"])
# # 結果を表示
# for text in texts:
#     score = scorer.get_perplexity(text)
#     if best_score > score:
#         best_score = score
#         best_text = text
