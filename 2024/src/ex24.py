from AdventOfCode import AdventOfCode
from enum import Enum


class Cmd(Enum):
    AND = lambda a, b: 1 if a + b == 2 else 0
    OR = lambda a, b: 1 if a + b > 0 else 0
    XOR = lambda a, b: 1 if a + b == 1 else 0

Cmd_map = {"AND": Cmd.AND, "OR": Cmd.OR, "XOR": Cmd.XOR}


def part1(data: list[str]):
    vals, fs = read_data(data)
    zkeys = sorted([v for v in fs.keys() if v[0] == 'z'], reverse=True)
    return calc(vals, fs, zkeys)


def part2(data: list[str]):
    vals, fs = read_data(data)


def calc(vals: dict[str, int], fs: dict[str,(str,Cmd,str)], zkeys: list[str]):
    missing_keys = set(fs.keys())
    while missing_keys:
        new_set = set()
        for key in missing_keys:
            f = fs[key]
            if f[0] in vals.keys() and f[2] in vals.keys():
                vals[key] = f[1](vals[f[0]], vals[f[2]])
            else:
                new_set.add(key)
        missing_keys = new_set
    return int("".join([str(vals[v]) for v in zkeys]), 2)



def read_data(data: list[str]) -> (dict[str, int], dict[str,(str,Cmd,str)]):
    res1, res2 = {}, {}
    for d in [d.strip() for d in data]:
        if ':' in d:
            line = d.split(": ")
            res1[line[0]] = int(line[1])
        elif " -> " in d:
            line = d.split(" -> ")
            command = line[0].split(" ")
            res2[line[1]] = command[0], Cmd_map[command[1]], command[2]
    return res1, res2


ex = AdventOfCode(24)
ex.executeTest(part1, 2024)

ex.execute(part1, part2)
