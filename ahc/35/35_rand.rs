use proconio::input_interactive;
use rand::prelude::*;
use rand::SeedableRng;
use rand_pcg::Pcg64Mcg;
use std::collections::HashSet;
use std::time::{Duration, Instant};

const N: usize = 6;
const M: usize = 15;
const T: usize = 10;
const NX: usize = 60;
const DIJ: [(i8, i8); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];

fn calc_score(tanes: &Vec<Vec<i32>>) -> i32 {
    assert_eq!(tanes.len(), NX, "len: {}", tanes.len());
    tanes
        .iter()
        .map(|tane| tane.iter().sum::<i32>())
        .max()
        .unwrap()
}

fn get_screened_tanes_idx(rng: &mut impl Rng) -> Vec<usize> {
    let mut indices: Vec<usize> = (0..NX).collect();
    indices.shuffle(rng);
    indices.truncate(N * N);
    indices
}

fn gen_field(screened_tanes_idx: &mut Vec<usize>) -> Vec<Vec<usize>> {
    (0..N)
        .map(|_| (0..N).map(|_| screened_tanes_idx.pop().unwrap()).collect())
        .collect()
}

fn gen_new_tanes(
    tanes: &Vec<Vec<i32>>,
    field: &Vec<Vec<usize>>,
    rng: &mut impl Rng,
) -> Vec<Vec<i32>> {
    let mut new_tanes = Vec::new();
    let mut visited = HashSet::new();
    for i in 0..N {
        for j in 0..N {
            for &(di, dj) in DIJ.iter() {
                let ni = i as i8 + di;
                let nj = j as i8 + dj;
                if ni < 0 || nj < 0 || ni >= N as i8 || nj >= N as i8 {
                    continue;
                }
                let idx1 = field[i][j];
                let idx2 = field[ni as usize][nj as usize];
                let pair = if idx1 < idx2 {
                    (idx1, idx2)
                } else {
                    (idx2, idx1)
                };
                if visited.contains(&pair) {
                    continue;
                }
                visited.insert(pair);
                let new_tane = (0..M)
                    .map(|k| {
                        if rng.gen_bool(0.5) {
                            tanes[idx1][k]
                        } else {
                            tanes[idx2][k]
                        }
                    })
                    .collect();
                new_tanes.push(new_tane);
            }
        }
    }
    new_tanes
}

fn main() {
    input_interactive! {
        _: usize, _: usize, _: usize,
    }

    let time_limit = Duration::from_secs_f64(1.98 / T as f64);
    let mut rng = Pcg64Mcg::from_entropy();
    for _ in 0..T {
        input_interactive! {
            mut init_tanes: [[i32; M];NX],
        }
        let mut max_score = i32::MIN;
        let mut max_field = Vec::new();
        let start_time = Instant::now();
        while start_time.elapsed() < time_limit {
            let mut tanes = init_tanes.clone();
            let mut sc_idx = get_screened_tanes_idx(&mut rng);
            let field = gen_field(&mut sc_idx);
            tanes = gen_new_tanes(&tanes, &field, &mut rng);
            let score = calc_score(&tanes);
            if score > max_score {
                max_score = score;
                max_field = field;
            }
        }
        for i in 0..N {
            for j in 0..N {
                print!("{} ", max_field[i][j]);
            }
            println!();
        }
    }
}
