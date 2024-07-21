#[derive(Debug)]
#[allow(dead_code)]
struct Tweedle {
    dee: u64,
    dum: u64,
}

fn swap_dum(t: &mut Tweedle, new_dum: u64) -> u64 {
    let prev_dum = t.dum;
    t.dum = new_dum;
    prev_dum
}

fn main() {
    let mut t = Tweedle {
        dee: 0x1234,
        dum: 0x5678,
    };

    let prev_dum = swap_dum(&mut t, 0x9abc);

    println!("Previous dum: {}", prev_dum);
}

