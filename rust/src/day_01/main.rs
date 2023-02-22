struct Elf {
    calories_list: Vec<i32>,
    total_calories: i32,
}

impl Elf {
    fn new(raw_data: &str) -> Elf {
        let mut elf = Elf {
            calories_list: Vec::new(),
            total_calories: 0,
        };

        elf.parse_data(raw_data);
        elf.calculate_total_calories();
        elf
    }

    fn parse_data(&mut self, raw_data: &str) {
        // Split on line breaks to seperate each elf calorie amount
        self.calories_list = raw_data
            .lines()
            .map(|calories| calories.parse::<i32>().unwrap())
            .collect();
    }

    fn calculate_total_calories(&mut self) {
        self.total_calories = self.calories_list.iter().sum();
    }
}

struct Elves {
    elves: Vec<Elf>,
}

impl Elves {
    fn new(input_data: String) -> Elves {
        let mut elves = Elves { elves: Vec::new() };

        elves.create_elves(input_data);
        elves.order_elves();
        elves
    }

    fn create_elves(&mut self, input_data: String) {
        // Split on blank lines to seperate each elf
        self.elves = input_data
            .split("\n\n")
            .map(|elf_raw_data| Elf::new(elf_raw_data))
            .collect();
    }

    fn order_elves(&mut self) {
        self.elves
            .sort_by(|a, b| b.total_calories.cmp(&a.total_calories));
    }

    fn get_top_elf_calories(&self) -> i32 {
        self.elves[0].total_calories
    }

    fn get_top_n_elves_calories_sum(&self, num_elves: usize) -> i32 {
        self.elves
            .iter()
            .take(num_elves)
            .map(|elf| elf.total_calories)
            .sum()
    }
}

pub fn main(input_data: String) -> (i32, i32) {
    let elves = Elves::new(input_data);

    let part_1_answer = elves.get_top_elf_calories();
    let part_2_answer = elves.get_top_n_elves_calories_sum(3);

    (part_1_answer, part_2_answer)
}
