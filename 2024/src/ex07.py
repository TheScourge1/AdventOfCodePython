from AdventOfCode import AdventOfCode
import math


def part1(data: list[str]):
    lines = read_data(data)
    return sum([ln[0] for ln in lines if is_true(ln,False)])


def part2(data: list[str]):
    lines = read_data(data)
    return sum([ln[0] for ln in lines if is_true(ln,True)])


def read_data(data: list[str]) -> list[(int, list[int])]:
    result = []
    for line in data:
        items = line.split(":")
        total = int(items[0])
        figures = [int(s) for s in items[1].strip().split(" ")]
        result.append((total, figures))
    return result


def is_true(line: (int, list[int]), part2: bool) -> bool:
    if len(line[1]) == 1:
        return line[0] == line[1][0]

    res_list = [line[1][0]]
    for nr in line[1][1:]:
        new_list = []
        for r in res_list:
            new_vals = [r+nr,r*nr]
            if part2:
                new_vals.append(r*int(math.pow(10, int(math.log(nr, 10))+1))+nr)
            new_list += [n for n in new_vals if n <= line[0]]
        res_list = new_list
    return res_list.count(line[0]) > 0


ex = AdventOfCode(7)
ex.executeTest(part1,3749)
ex.executeTest(part2, 11387)

ex.execute(part1, part2)