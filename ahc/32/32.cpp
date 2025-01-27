#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 998244353;
static const int BEAM_WIDTH = 23;

int N, M, K;
static vector<vector<long long>> graphData;
static vector<vector<vector<long long>>> stamps;

long long calc_score() {
  long long score = 0;
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      score += (graphData[i][j] % MOD);
    }
  }
  return score;
}

void add_value(int m, int p, int q) {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      graphData[p + i][q + j] += stamps[m][i][j];
    }
  }
}

void restore_value(int m, int p, int q) {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      graphData[p + i][q + j] -= stamps[m][i][j];
    }
  }
}

struct State {
  long long negScore;
  vector<array<int, 3>> moves;
};

bool operator<(const State &a, const State &b) {
  return a.negScore < b.negScore;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> N >> M >> K;

  graphData.assign(N, vector<long long>(N, 0LL));
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      cin >> graphData[i][j];
    }
  }

  stamps.assign(M, vector<vector<long long>>(3, vector<long long>(3, 0LL)));
  for (int m_idx = 0; m_idx < M; m_idx++) {
    for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
        cin >> stamps[m_idx][i][j];
      }
    }
  }

  vector<State> solutions;
  solutions.push_back({0, {}});

  for (int _ = 0; _ < K; _++) {
    vector<State> candidates;

    for (auto &score_sol : solutions) {
      long long current_score = score_sol.negScore;
      auto &cur_sol = score_sol.moves;

      for (int m_idx = 0; m_idx < M; m_idx++) {
        for (int i = 0; i < N - 2; i++) {
          for (int j = 0; j < N - 2; j++) {
            vector<array<int, 3>> new_solution = cur_sol;
            new_solution.push_back({m_idx, i, j});

            int n = (int)new_solution.size();
            for (int cs = 0; cs < n; cs++) {
              auto &mv = new_solution[cs];
              add_value(mv[0], mv[1], mv[2]);
            }

            long long score = calc_score();

            for (int cs = 0; cs < n; cs++) {
              auto &mv = new_solution[cs];
              restore_value(mv[0], mv[1], mv[2]);
            }

            State st;
            st.negScore = -score;
            st.moves = new_solution;
            candidates.push_back(st);
          }
        }
      }
    }

    sort(candidates.begin(), candidates.end());

    while ((int)candidates.size() > BEAM_WIDTH) {
      candidates.pop_back();
    }

    solutions = candidates;
  }

  auto &best = solutions[0];
  cout << best.moves.size() << endl;
  for (auto &mv : best.moves) {
    cout << mv[0] << " " << mv[1] << " " << mv[2] << endl;
  }

  return 0;
}
