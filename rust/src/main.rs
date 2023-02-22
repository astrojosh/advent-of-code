use std::env;
use std::fs;
use std::path::Path;

#[path = "day_01/main.rs"]
mod day_01;
#[path = "day_02/main.rs"]
mod day_02;

fn read_data(file_path: String) -> String {
    let data = fs::read_to_string(format!("../data/{file_path}")).expect("Reading example input");
    data.strip_suffix("\n").unwrap().to_string()
}

fn test_section(path: String, module: fn(String) -> (i32, i32), section: i32, debug: bool) {
    let example_input = read_data(format!("example_input/{path}.txt"));

    let answer = match section {
        1 => module(example_input).0,
        2 => module(example_input).1,
        _ => panic!("Unexpected section"),
    };

    let example_output = read_data(format!("example_output/{path}.txt"));

    let expected_answer = match section {
        1 => example_output.split(",").collect::<Vec<&str>>()[0],
        2 => example_output.split(",").collect::<Vec<&str>>()[1],
        _ => panic!("Unexpected section"),
    };

    if !debug {
        assert_eq!(answer.to_string(), expected_answer);
    }
}

fn run_tests(day: &str, module: fn(String) -> (i32, i32), debug: bool) {
    println!("Running code on test data");

    let mut part_1_path = day.to_string();
    let mut part_2_path = day.to_string();

    if Path::new(format!("../data/example_input/{day}_part_1.txt").as_str()).exists() {
        part_1_path = format!("{day}_part_1");
        part_2_path = format!("{day}_part_2");
    }

    test_section(part_1_path, module, 1, debug);

    if !debug {
        test_section(part_2_path, module, 2, debug);
        println!("Tests passed successfully\n");
    }
}

fn run(day: &str, module: fn(String) -> (i32, i32)) {
    println!("Running code on input data");

    let input_data = read_data(format!("input/{day}.txt"));
    let (part_1_answer, part_2_answer) = module(input_data);

    println!("Part 1 Answer = {part_1_answer}");
    println!("Part 2 Answer = {part_2_answer}");
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let day = &args[1];

    let module = match day.as_str() {
        "day_01" => day_01::main,
        "day_02" => day_02::main,
        _ => panic!("Module not found"),
    };

    if args.len() == 3 && &args[2] == "debug" {
        run_tests(day, module, true);
    } else {
        run_tests(day, module, false);
        run(day, module);
    }
}
