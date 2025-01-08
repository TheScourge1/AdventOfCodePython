from AdventOfCode import AdventOfCode
import re


def part1(data: list):
    all_data = ""
    for line in data:
        all_data += line
    mul_pattern = r'mul\(\d+,\d+\)'
    matches = re.findall(mul_pattern, all_data)
    numbers = ([match[4:len(match)-1].split(",") for match in matches])
    return sum(int(n[0])*int(n[1]) for n in numbers)


def part2(data: list):
    all_data = ""
    for line in data:
        all_data += line
    mul_pattern = r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)'
    matches = re.findall(mul_pattern, all_data)
    keep = True
    filtered_matches = []
    for match in matches:
        if keep and str(match).startswith("mul"):
            filtered_matches.append(match)
        elif match == "do()":
            keep = True
        elif match == "don't()":
            keep = False
    numbers = ([match[4:len(match)-1].split(",") for match in filtered_matches])
    return sum(int(n[0])*int(n[1]) for n in numbers)


ex = AdventOfCode(3)
ex.executeTest(part1,161)
ex.executeTest(part2,48,2)

ex.execute(part1, part2)
