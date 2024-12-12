use std::collections::HashMap;
use std::fs;

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

    let mut c = HashMap::new();
    for value in second {
        *c.entry(value).or_insert(0) += 1;
    }

    let s: i64 = first.iter().map(|v| v * *c.entry(*v).or_insert(0)).sum();
    println!("{s}");
}
