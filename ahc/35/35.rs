use proconio::input_interactive;
use rand::seq::SliceRandom;
use rand::Rng;
use std::collections::{HashSet, VecDeque};
use std::time::Instant;

const N: usize = 6;
const M: usize = 15;
const T: usize = 10;
const NX: usize = 60;
const DIJ: [(i32, i32); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];
const START_TEMPERATURE: f64 = 50.0;
const END_TEMPERATURE: f64 = 20.0;
const TIME_LIMIT: f64 = 1.99 / T as f64;
const CORNERS: &[(usize, usize)] = &[(0, 0), (5, 0), (0, 5), (5, 5)];
const EDGES: &[(usize, usize)] = &[
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (1, 5),
    (2, 5),
    (3, 5),
    (4, 5),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
];

fn calc_score(tanes: &Vec<Vec<i32>>) -> i32 {
    tanes.iter().map(|tane| tane.iter().sum()).max().unwrap()
}

fn generate_new_tanes(
    tanes: &Vec<Vec<i32>>,
    field: &Vec<Vec<usize>>,
    rng: &mut impl Rng,
) -> Vec<Vec<i32>> {
    let mut new_tanes = Vec::new();
    let mut visited = HashSet::new();
    for i in 0..N {
        for j in 0..N {
            for &(di, dj) in &DIJ {
                let ni = i as i32 + di;
                let nj = j as i32 + dj;
                if ni < 0 || nj < 0 || ni >= N as i32 || nj >= N as i32 {
                    continue;
                }
                let ni = ni as usize;
                let nj = nj as usize;
                let idx1 = field[i][j];
                let idx2 = field[ni][nj];
                let pair = if idx1 < idx2 {
                    (idx1, idx2)
                } else {
                    (idx2, idx1)
                };
                if visited.contains(&pair) {
                    continue;
                }
                visited.insert(pair);

                let mut new_tane = Vec::with_capacity(M);
                for k in 0..M {
                    let value = if rng.gen_bool(0.5) {
                        tanes[idx1][k]
                    } else {
                        tanes[idx2][k]
                    };
                    new_tane.push(value);
                }
                new_tanes.push(new_tane);
            }
        }
    }
    new_tanes
}

fn swap_field_elements(max_field: &mut Vec<Vec<usize>>, rng: &mut impl Rng) -> Vec<Vec<usize>> {
    let mut swap = Vec::new();
    let q = rand::thread_rng().gen_range(0..3);
    if q == 1 {
        while swap.len() < 2 {
            let i = rng.gen_range(0..N);
            let j = rng.gen_range(0..N);
            if EDGES.contains(&(i, j)) || CORNERS.contains(&(i, j)) {
                continue;
            }
            swap.push((i, j));
        }
    } else if q == 1 {
        swap = EDGES
            .choose_multiple(&mut rand::thread_rng(), 2)
            .cloned()
            .collect();
    } else if q == 2 {
        swap = CORNERS
            .choose_multiple(&mut rand::thread_rng(), 2)
            .cloned()
            .collect();
    }
    let mut swapped_field = max_field.clone();
    if let [(i1, j1), (i2, j2)] = swap.as_slice() {
        let tmp = swapped_field[*i1][*j1];
        swapped_field[*i1][*j1] = swapped_field[*i2][*j2];
        swapped_field[*i2][*j2] = tmp;
    }
    swapped_field
}

fn zscore_sorted_idx(tanes: &Vec<Vec<i32>>) -> VecDeque<usize> {
    let mut vec_j = vec![Vec::with_capacity(NX); M];
    for i in 0..NX {
        for j in 0..M {
            vec_j[j].push(tanes[i][j] as f64);
        }
    }

    let mut zscores = Vec::with_capacity(M);
    for j in 0..M {
        let data = &vec_j[j];
        let n = data.len() as f64;
        let mean = data.iter().sum::<f64>() / n;
        let variance = data.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / (n - 1 as f64);
        let stddev = variance.sqrt();
        let zscore = data
            .iter()
            .map(|&x| {
                if stddev == 0.0 {
                    0.0
                } else {
                    let z = (x - mean) / stddev;
                    if z > 0.0 {
                        z.powi(3)
                    } else {
                        z
                    }
                }
            })
            .collect::<Vec<f64>>();
        zscores.push(zscore);
    }

    let mut tot_zscore = vec![0.0; NX];
    for j in 0..M {
        for i in 0..NX {
            tot_zscore[i] += zscores[j][i];
        }
    }
    let mut indices: Vec<usize> = (0..NX).collect();
    indices.sort_by(|&a, &b| tot_zscore[a].partial_cmp(&tot_zscore[b]).unwrap());
    VecDeque::from(indices)
}

fn create_field(z_sorted_idx: &mut VecDeque<usize>) -> Vec<Vec<usize>> {
    let mut field = vec![vec![0; N]; N];
    for i in 0..N {
        for j in 0..N {
            if EDGES.contains(&(i, j)) || CORNERS.contains(&(i, j)) {
                continue;
            }
            field[i][j] = z_sorted_idx.pop_back().unwrap();
        }
    }
    for &(i, j) in EDGES.iter() {
        field[i][j] = z_sorted_idx.pop_back().unwrap();
    }
    for &(i, j) in CORNERS.iter() {
        field[i][j] = z_sorted_idx.pop_back().unwrap();
    }
    field
}

fn main() {
    input_interactive! {
        _: usize, _: usize, _: usize,
    }

    let mut rng = rand::thread_rng();
    for _ in 0..T {
        input_interactive! {
            mut tanes: [[i32; M]; NX],
        }
        let start_time = Instant::now();
        let mut max_score = calc_score(&tanes);
        let mut z_sorted_idx = zscore_sorted_idx(&tanes);
        let mut max_field = create_field(&mut z_sorted_idx);

        while start_time.elapsed().as_secs_f64() < TIME_LIMIT {
            let swapped_field = swap_field_elements(&mut max_field, &mut rng);
            let new_tanes = generate_new_tanes(&tanes, &swapped_field, &mut rng);
            let new_score = calc_score(&new_tanes);
            let dt = start_time.elapsed().as_secs_f64();
            let temp = START_TEMPERATURE + (END_TEMPERATURE - START_TEMPERATURE) * dt / TIME_LIMIT;
            let delta_score = max_score - new_score;
            if f64::exp(delta_score as f64 / temp) > rng.gen::<f64>() {
                max_score = new_score;
                max_field = swapped_field.clone();
            }
        }

        // Output max_field
        for j in 0..N {
            for k in 0..N {
                print!("{} ", max_field[j][k]);
            }
            println!();
        }
    }
}
