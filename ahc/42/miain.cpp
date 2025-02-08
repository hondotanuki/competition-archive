#include <bits/stdc++.h>
using namespace std;

int N;
vector<vector<char>> G;
int oni, fuku;

void minus_fuku_or_oni(char element) {
  if (element == 'o') {
    fuku -= 1;
  } else if (element == 'x') {
    oni -= 1;
  }
}

int calc_official_score(int T) {
  assert(oni >= 0 && fuku >= 0);
  if (oni == 0 && fuku == 0) {
    return 8 * N * N - T;
  } else {
    return 4 * N * N - N * (oni + 40 - fuku);
  }
}

void move_graph(char dir, int idx) {
  assert(dir == 'L' || dir == 'R' || dir == 'U' || dir == 'D');
  assert(0 <= idx && idx < N);

  if (dir == 'L') {
    minus_fuku_or_oni(G[idx][0]);

    for (int j = 0; j < N - 1; j++) {
      G[idx][j] = G[idx][j + 1];
    }
    G[idx][N - 1] = '.';
  } else if (dir == 'R') {
    minus_fuku_or_oni(G[idx][N - 1]);

    for (int j = N - 1; j > 0; j--) {
      G[idx][j] = G[idx][j - 1];
    }
    G[idx][0] = '.';
  } else if (dir == 'U') {
    minus_fuku_or_oni(G[0][idx]);

    for (int i = 0; i < N - 1; i++) {
      G[i][idx] = G[i + 1][idx];
    }
    G[N - 1][idx] = '.';
  } else if (dir == 'D') {
    minus_fuku_or_oni(G[N - 1][idx]);

    for (int i = N - 1; i > 0; i--) {
      G[i][idx] = G[i - 1][idx];
    }
    G[0][idx] = '.';
  }
}
struct MoveScoreDetail {
  double score;
  char direction;
  int idx;
  int times;
};

MoveScoreDetail calc_move_score(int i, int j) {
  auto countFunc = [&](int r, int c, int cnt) {
    if (G[r][c] == 'o') {
      cnt -= 1;
    } else if (G[r][c] == 'x') {
      cnt += 1;
    }
    return cnt;
  };

  int count_l = 0, count_r = 0, count_u = 0, count_d = 0;
  for (int m = 1; m < N; m++) {
    if (j - m >= 0) {
      count_l = countFunc(i, j - m, count_l);
    }
    if (j + m < N) {
      count_r = countFunc(i, j + m, count_r);
    }
    if (i - m >= 0) {
      count_u = countFunc(i - m, j, count_u);
    }
    if (i + m < N) {
      count_d = countFunc(i + m, j, count_d);
    }
  }

  double score_l = (j + 1 == 0) ? 0.0 : (double)count_l / (double)(j + 1);
  double score_r = (N - j == 0) ? 0.0 : (double)count_r / (double)(N - j);
  double score_u = (i + 1 == 0) ? 0.0 : (double)count_u / (double)(i + 1);
  double score_d = (N - j == 0) ? 0.0 : (double)count_d / (double)(N - j);

  double max_score = max({score_l, score_r, score_u, score_d});

  MoveScoreDetail result;
  result.score = max_score;
  if (fabs(max_score - score_l) < 1e-9) {
    result.direction = 'L';
    result.idx = i;
    result.times = j + 1;
  } else if (fabs(max_score - score_r) < 1e-9) {
    result.direction = 'R';
    result.idx = i;
    result.times = (N - j);
  } else if (fabs(max_score - score_u) < 1e-9) {
    result.direction = 'U';
    result.idx = j;
    result.times = (i + 1);
  } else {
    result.direction = 'D';
    result.idx = j;
    result.times = (N - i);
  }
  return result;
}

vector<MoveScoreDetail> get_good_move() {
  vector<MoveScoreDetail> moves;
  moves.reserve(N * N);

  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      if (G[i][j] == 'x') {
        MoveScoreDetail msd = calc_move_score(i, j);
        moves.push_back(msd);
      }
    }
  }
  sort(moves.begin(), moves.end(),
       [&](auto &a, auto &b) { return a.score > b.score; });
  return moves;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> N;
  G.resize(N, vector<char>(N));
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      cin >> G[i][j];
    }
  }

  oni = 2 * N;
  fuku = 2 * N;

  vector<vector<char>> ori = G;

  int best_score = -1;
  vector<pair<char, int>> best_ans;
  vector<array<int, 4>> order;
  order.reserve(625);
  for (int a = 0; a < 5; a++) {
    for (int b = 0; b < 5; b++) {
      for (int c = 0; c < 5; c++) {
        for (int d = 0; d < 5; d++) {
          order.push_back({a, b, c, d});
        }
      }
    }
  }
  auto st = chrono::steady_clock::now();

  for (int i = 0; i < (int)order.size(); i++) {
    {
      auto now = chrono::steady_clock::now();
      double elapsed = chrono::duration<double>(now - st).count();
      if (elapsed > 1.8) {
        break;
      }
    }

    G = ori;
    oni = 40;
    fuku = 40;
    int T = 0;
    vector<pair<char, int>> ans;
    int j = 0;
    while (oni > 0 && T < 4 * N * N) {
      vector<MoveScoreDetail> moves = get_good_move();
      if (moves.empty()) break;

      int o = 0;
      if (j < 4) {
        o = order[i][j];
        if (o < 0 || o >= (int)moves.size()) {
          o = 0;
        }
      }
      MoveScoreDetail msd = moves[o];

      char direction = msd.direction;
      int idx = msd.idx;
      int times = msd.times;

      for (int _t = 0; _t < times; _t++) {
        move_graph(direction, idx);
        ans.push_back({direction, idx});
        T++;
        if (T >= 4 * N * N) break;
        if (oni <= 0) break;
      }
      j++;
    }

    int score = calc_official_score(T);
    if (score > best_score) {
      best_score = score;
      best_ans = ans;
    }
  }

  for (auto &p : best_ans) {
    cout << p.first << " " << p.second << "\n";
  }

  return 0;
}
