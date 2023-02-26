struct Range {
    lower_bound: i32,
    upper_bound: i32,
}

impl Range {
    fn new(lower_bound: i32, upper_bound: i32) -> Self {
        Self {
            lower_bound: lower_bound,
            upper_bound: upper_bound,
        }
    }

    fn contains(&self, range: &Range) -> bool {
        let condition_1 = self.lower_bound <= range.lower_bound;
        let condition_2 = range.upper_bound <= self.upper_bound;
        condition_1 && condition_2
    }

    fn overlaps(&self, range: &Range) -> bool {
        let condition_1 = self.lower_bound <= range.upper_bound;
        let condition_2 = range.lower_bound <= self.upper_bound;
        condition_1 && condition_2
    }
}

fn line_to_ranges(input_line: &str) -> (Range, Range) {
    let raw_range = input_line.split(",").collect::<Vec<_>>();

    assert_eq!(raw_range.len(), 2);
    let (raw_range_1, raw_range_2) = (raw_range[0], raw_range[1]);

    let bounds_1 = raw_range_1
        .split("-")
        .map(|bound| bound.parse::<i32>().unwrap())
        .collect::<Vec<_>>();

    assert_eq!(bounds_1.len(), 2);
    let (lower_bound_1, upper_bound_1) = (bounds_1[0], bounds_1[1]);

    let bounds_2 = raw_range_2
        .split("-")
        .map(|bound| bound.parse::<i32>().unwrap())
        .collect::<Vec<_>>();

    assert_eq!(bounds_2.len(), 2);
    let (lower_bound_2, upper_bound_2) = (bounds_2[0], bounds_2[1]);

    let range_1 = Range::new(lower_bound_1, upper_bound_1);
    let range_2 = Range::new(lower_bound_2, upper_bound_2);

    (range_1, range_2)
}

fn contained(range_1: &Range, range_2: &Range) -> bool {
    range_1.contains(range_2) || range_2.contains(range_1)
}

pub fn main(input_data: String) -> (i32, i32) {
    let range_pairs = input_data
        .lines()
        .map(|input_line| line_to_ranges(input_line));

    let part_1_answer = range_pairs
        .clone()
        .map(|(range_1, range_2)| contained(&range_1, &range_2) as i32)
        .sum();

    let part_2_answer = range_pairs
        .map(|(range_1, range_2)| range_1.overlaps(&range_2) as i32)
        .sum();

    (part_1_answer, part_2_answer)
}
