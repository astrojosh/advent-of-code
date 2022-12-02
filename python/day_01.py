with open("../data/day_01") as f:
    data = f.read()

# Remove trailing new line and split on blank lines to seperate calories from each elf
cleaned_data = data.rstrip().split("\n\n")

# Split on line breaks to seperate each elf calorie amount and convert to an integer
elf_calories = [map(int, x.split("\n")) for x in cleaned_data]

elf_totals = map(sum, elf_calories)

top_elves = sorted(elf_totals, reverse=True)[:3]

print(max(top_elves), sum(top_elves))
