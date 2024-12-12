use std::fs;
use std::iter::zip;

fn main() {
    let mut first = Vec::new();
    let mut second = Vec::new();

    for line in fs::read_to_string("day01/input.txt").unwrap().lines() {
        if let Some((a, b)) = line.split_once("   ") {
            let a_int: i64 = a.parse().unwrap();
            let b_int: i64 = b.parse().unwrap();
            first.push(a_int);
            second.push(b_int);
        }
    }

    first.sort();
    second.sort();

    let s: i64 = zip(first, second).map(|x| (x.0 - x.1).abs()).sum();
    println!("{s}");
}
