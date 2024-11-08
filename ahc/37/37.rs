use proconio::input;
use std::collections::BTreeSet;

type Node = (i64, i64);

// 解説通りの評価関数
fn calc_score(u: &Node, v: &Node) -> i64 {
    (u.0.abs_diff(v.0) as i64) + (u.1.abs_diff(v.1) as i64) - (u.0 + u.1 + v.0 + v.1)
}

fn main() {
    input! {
        n: u16,
        pairs:[(i64, i64); n],
    }
    let mut nodes: BTreeSet<Node> = pairs.into_iter().collect();
    let mut rev_soda: Vec<[i64; 4]> = Vec::new();

    // ノードが1つになるまで繰り返す
    while nodes.len() != 1 {
        let mut min_score = i64::MAX;
        let mut min_score_u: Option<Node> = None;
        let mut min_score_v: Option<Node> = None;

        // 毎回クローンした方が早い
        let node_vec: Vec<Node> = nodes.iter().cloned().collect();
        let current_len = node_vec.len();

        for i in 0..current_len {
            for j in (i + 1)..current_len {
                let score = calc_score(&node_vec[i], &node_vec[j]);
                if score < min_score {
                    min_score = score;
                    min_score_u = Some(node_vec[i]);
                    min_score_v = Some(node_vec[j]);
                }
            }
        }

        let u = min_score_u.unwrap();
        let v = min_score_v.unwrap();

        // 補助ノードはペアのminx, miny
        let aux_x = if u.0 < v.0 { u.0 } else { v.0 };
        let aux_y = if u.1 < v.1 { u.1 } else { v.1 };
        let aux_node = (aux_x, aux_y);

        // nodesからuとvを削除、補助点を追加
        assert!(nodes.remove(&u), "nodesにuがない");
        assert!(nodes.remove(&v), "nodesにvがない");
        nodes.insert(aux_node);

        // 解答へ追加
        if aux_node != u {
            rev_soda.push([aux_node.0, aux_node.1, u.0, u.1]);
        }
        if aux_node != v {
            rev_soda.push([aux_node.0, aux_node.1, v.0, v.1]);
        }
    }

    // 最後の一点は結べないので手動で結ぶ
    if let Some(&(x, y)) = nodes.iter().next() {
        if x != 0 || y != 0 {
            rev_soda.push([0, 0, x, y]);
        }
    }

    let m = rev_soda.len();
    println!("{}", m);
    for soda in rev_soda.iter().rev() {
        println!("{} {} {} {}", soda[0], soda[1], soda[2], soda[3]);
    }
}
