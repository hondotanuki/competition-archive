#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cassert>
#include <set>
#include <ctime>
#include <cstdlib>
#include <climits>

using namespace std;

int n, m, t;
int n_x;
vector<pair<int, int>> dij = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

int calc_score(const vector<vector<int>>& tanes) {
    assert(tanes.size() == n_x);
    int max_sum = INT_MIN;
    for (const auto& tane : tanes) {
        int sum = accumulate(tane.begin(), tane.end(), 0);
        if (sum > max_sum) max_sum = sum;
    }
    return max_sum;
}

vector<int> get_screened_tanes_idx() {
    vector<int> indices(n_x);
    iota(indices.begin(), indices.end(), 0);
    random_shuffle(indices.begin(), indices.end());
    vector<int> screened_tanes_idx(indices.begin(), indices.begin() + n * n);
    return screened_tanes_idx;
}

vector<vector<int>> gen_field(const vector<int>& screened_tanes_idx) {
    vector<vector<int>> field(n, vector<int>(n));
    int idx = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            field[i][j] = screened_tanes_idx[idx++];
        }
    }
    return field;
}

vector<vector<int>> gen_new_tanes(const vector<vector<int>>& tanes, const vector<vector<int>>& field) {
    vector<vector<int>> new_tanes;
    set<pair<int, int>> visited;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            for (const auto& d : dij) {
                int di = d.first;
                int dj = d.second;
                int ni = i + di;
                int nj = j + dj;
                if (ni < 0 || nj < 0 || ni >= n || nj >= n) continue;
                int idx1 = field[i][j];
                int idx2 = field[ni][nj];
                int min_idx = min(idx1, idx2);
                int max_idx = max(idx1, idx2);
                pair<int, int> p = make_pair(min_idx, max_idx);
                if (visited.count(p)) continue;
                visited.insert(p);

                vector<int> new_tane(m);
                for (int k = 0; k < m; ++k) {
                    if (rand() % 2 == 0) {
                        new_tane[k] = tanes[idx1][k];
                    } else {
                        new_tane[k] = tanes[idx2][k];
                    }
                }
                new_tanes.push_back(new_tane);
            }
        }
    }
    return new_tanes;
}

int main() {
    srand(time(0));
    cin >> n >> m >> t;
    n_x = 2 * n * (n - 1);
    vector<vector<int>> init_tanes(n_x, vector<int>(m));
    for (int i = 0; i < n_x; ++i) {
        for (int j = 0; j < m; ++j) {
            cin >> init_tanes[i][j];
        }
    }

    clock_t start_time = clock();
    double time_limit = 1.5;
    int max_score = -1;
    vector<vector<int>> max_field;
    vector<vector<int>> tanes;
    int score = 0;
    while ((double)(clock() - start_time) / CLOCKS_PER_SEC < time_limit) {
        tanes = init_tanes;
        vector<vector<int>> field;
        vector<vector<int>> field_0;
        for (int i = 0; i < t; ++i) {
            vector<int> sc_idx = get_screened_tanes_idx();
            field = gen_field(sc_idx);
            tanes = gen_new_tanes(tanes, field);
            score = calc_score(tanes);
            if (i == 0) {
                field_0 = field;
            }
        }
        if (score > max_score) {
            max_score = score;
            max_field = field_0;
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << max_field[i][j];
            if (j != n - 1) cout << " ";
        }
        cout << endl;
    }
    return 0;
}
