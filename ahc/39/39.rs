use proconio::input;
use rand::Rng;
use std::time::Instant;

fn gen_rec() -> Vec<(i32, i32)> {
    let mut rng = rand::thread_rng();
    loop {
        let x = rng.gen_range(0..=100_000);
        let y = rng.gen_range(0..=100_000);
        let width = rng.gen_range(500..=100_000);
        let height = rng.gen_range(500..=100_000);

        if x >= width && y >= height {
            return vec![
                (x, y),
                (x, y - height),
                (x - width, y - height),
                (x - width, y),
            ];
        }
    }
}
fn is_point_inside_polygon(maxx: i32, minx: i32, maxy: i32, miny: i32, x: i32, y: i32) -> bool {
    minx <= x && x <= maxx && miny <= y && y <= maxy
}

fn main() {
    input! {
        n: u16,
        sabas:[(i32, i32); n],
        iwashis:[(i32, i32); n],
    }

    let time_limit = 1.98;
    let start_time = Instant::now();

    let mut max_cnt = -1;
    let mut max_rec: Vec<(i32, i32)> = Vec::new();

    while start_time.elapsed().as_secs_f64() < time_limit {
        let mut cnt = 0;
        let rec = gen_rec();

        let mut maxx = -1;
        let mut minx = i32::MAX;
        let mut maxy = -1;
        let mut miny = i32::MAX;

        for &(x, y) in &rec {
            maxx = std::cmp::max(maxx, x);
            minx = std::cmp::min(minx, x);
            maxy = std::cmp::max(maxy, y);
            miny = std::cmp::min(miny, y);
        }

        for &(x, y) in &sabas {
            if is_point_inside_polygon(maxx, minx, maxy, miny, x, y) {
                cnt += 1;
            }
        }

        for &(x, y) in &iwashis {
            if is_point_inside_polygon(maxx, minx, maxy, miny, x, y) {
                cnt -= 1;
            }
        }

        if cnt > max_cnt {
            max_cnt = cnt;
            max_rec = rec.clone();
        }
    }

    println!("{}", max_rec.len());
    for &(x, y) in &max_rec {
        println!("{} {}", x, y);
    }
}
