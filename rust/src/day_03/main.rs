use std::collections::HashSet;

#[derive(Clone, Copy)]
struct Item {
    character: char,
    priority: i32,
}

impl Item {
    fn new(character: char) -> Self {
        let mut item = Self {
            character: character,
            priority: i32::default(),
        };

        item.calculate_priority();
        item
    }

    fn calculate_priority(&mut self) {
        if self.character.is_uppercase() {
            self.priority = (self.character as i32) - ('A' as i32) + 27;
        } else {
            self.priority = (self.character as i32) - ('a' as i32) + 1;
        }
    }
}

#[derive(Clone)]
struct Rucksack {
    contents: String,
    compartment_1: String,
    compartment_2: String,
}

impl Rucksack {
    fn new(contents: &str) -> Self {
        let mut rucksack = Self {
            contents: contents.to_string(),
            compartment_1: String::default(),
            compartment_2: String::default(),
        };

        rucksack.split_contents_into_compartments();
        rucksack
    }

    fn split_contents_into_compartments(&mut self) {
        let num_contents = self.contents.len();
        let midpoint = num_contents / 2;
        let (compartment_1, compartment_2) = self.contents.split_at(midpoint);
        self.compartment_1 = compartment_1.to_string();
        self.compartment_2 = compartment_2.to_string();
    }

    fn get_common_item(&self) -> Item {
        let item_strings = vec![self.compartment_1.clone(), self.compartment_2.clone()];
        get_common_item(item_strings)
    }
}

struct Group {
    rucksacks: Vec<Rucksack>,
}

impl Group {
    fn new(rucksacks: Vec<Rucksack>) -> Self {
        Self {
            rucksacks: rucksacks,
        }
    }

    fn get_common_item(&self) -> Item {
        let item_strings = self
            .rucksacks
            .iter()
            .map(|rucksack| rucksack.to_owned().contents)
            .collect();

        get_common_item(item_strings)
    }
}

fn get_common_items(item_strings: Vec<String>) -> Vec<Item> {
    let mut common_items_set = HashSet::from_iter(item_strings[0].chars());

    let item_sets = item_strings[1..]
        .iter()
        .map(|item_string| HashSet::from_iter(item_string.chars()));

    for item_set in item_sets {
        common_items_set = common_items_set
            .intersection(&item_set)
            .map(|i| *i)
            .collect::<HashSet<_>>();
    }

    let common_items = common_items_set.iter().map(|i| Item::new(*i)).collect();

    common_items
}

fn get_common_item(item_strings: Vec<String>) -> Item {
    let common_items = get_common_items(item_strings);
    assert_eq!(common_items.len(), 1);
    common_items[0]
}

pub fn main(input_data: String) -> (i32, i32) {
    let rucksacks = input_data.lines().map(|contents| Rucksack::new(contents));

    let part_1_answer = rucksacks
        .clone()
        .map(|rucksack| rucksack.get_common_item().priority)
        .sum();

    let num_elves_per_group = 3;

    let rucksacks_vec = rucksacks.collect::<Vec<_>>();

    let groups = rucksacks_vec
        .chunks(num_elves_per_group)
        .map(|rucksacks| Group::new(rucksacks.to_owned()));

    let part_2_answer = groups.map(|group| group.get_common_item().priority).sum();

    (part_1_answer, part_2_answer)
}
