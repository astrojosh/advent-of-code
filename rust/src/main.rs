use std::env;
use std::fs;
use std::path::Path;

#[path = "day_01/main.rs"]
mod day_01;
#[path = "day_02/main.rs"]
mod day_02;
#[path = "day_03/main.rs"]
mod day_03;
#[path = "day_04/main.rs"]
mod day_04;
#[path = "day_05/main.rs"]
mod day_05;
#[path = "day_06/main.rs"]
mod day_06;
#[path = "day_07/main.rs"]
mod day_07;
#[path = "day_08/main.rs"]
mod day_08;
#[path = "day_09/main.rs"]
mod day_09;
#[path = "day_10/main.rs"]
mod day_10;
#[path = "day_11/main.rs"]
mod day_11;
#[path = "day_12/main.rs"]
mod day_12;
#[path = "day_13/main.rs"]
mod day_13;
#[path = "day_14/main.rs"]
mod day_14;
#[path = "day_15/main.rs"]
mod day_15;
#[path = "day_16/main.rs"]
mod day_16;
#[path = "day_17/main.rs"]
mod day_17;
#[path = "day_18/main.rs"]
mod day_18;
#[path = "day_19/main.rs"]
mod day_19;
#[path = "day_20/main.rs"]
mod day_20;
#[path = "day_21/main.rs"]
mod day_21;
#[path = "day_22/main.rs"]
mod day_22;
#[path = "day_23/main.rs"]
mod day_23;
#[path = "day_24/main.rs"]
mod day_24;
#[path = "day_25/main.rs"]
mod day_25;

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
        "day_03" => day_03::main,
        "day_04" => day_04::main,
        "day_05" => day_05::main,
        "day_06" => day_06::main,
        "day_07" => day_07::main,
        "day_08" => day_08::main,
        "day_09" => day_09::main,
        "day_10" => day_10::main,
        "day_11" => day_11::main,
        "day_12" => day_12::main,
        "day_13" => day_13::main,
        "day_14" => day_14::main,
        "day_15" => day_15::main,
        "day_16" => day_16::main,
        "day_17" => day_17::main,
        "day_18" => day_18::main,
        "day_19" => day_19::main,
        "day_20" => day_20::main,
        "day_21" => day_21::main,
        "day_22" => day_22::main,
        "day_23" => day_23::main,
        "day_24" => day_24::main,
        "day_25" => day_25::main,
        _ => panic!("Module not found"),
    };

    if args.len() == 3 && &args[2] == "debug" {
        run_tests(day, module, true);
    } else {
        run_tests(day, module, false);
        run(day, module);
    }
}
