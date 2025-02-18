from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import re


@dataclass
class ClawMachine:
    button_a: (int,int)
    button_b: (int,int)
    prize_loc: (int,int)


def part1(data: list[str]):
    machines = read_data(data)

    return sum([ 3*calc_token(m)[0]+calc_token(m)[1] for m in machines])


def part2(data: list[str]):
    machines = read_data(data)

    for m in machines:
        m.prize_loc = (m.prize_loc[0]+10000000000000,m.prize_loc[1]+10000000000000)

    return sum([ 3*calc_token(m)[0]+calc_token(m)[1] for m in machines])


def read_data(data:list[str]) -> list[ClawMachine]:
    pattern_nr = r'\d+'
    result = []
    for i in range(0,len(data)//4+1):
        a = tuple(map(int, re.findall(pattern_nr, data[4*i])))
        b = tuple(map(int, re.findall(pattern_nr, data[4*i+1])))
        prize = tuple(map(int, re.findall(pattern_nr, data[4*i+2])))
        result.append(ClawMachine(a, b, prize))
    return result


def min_token_cost(m: ClawMachine) -> int:
    results = []
    for i in range(0, 100):
        for j in range(0, 100):
            if (m.prize_loc[0] == m.button_a[0]*i + m.button_b[0]*j
                    and m.prize_loc[1] == m.button_a[1]*i + m.button_b[1]*j):
                results.append(3*i+j)
    if len (results) == 0:
        return 0
    return min(results)


def calc_token(m:ClawMachine) -> (int, int):
    p = m.prize_loc
    a = m.button_a
    b = m.button_b

    x2 = (p[0]*a[1] - p[1]*a[0]) // (b[0]*a[1]-b[1]*a[0])
    x1 = (p[0]*b[1] - p[1]*b[0]) // (b[1]*a[0]-b[0]*a[1])

    if p[0] == x1 * a[0] + x2 *b[0] and  p[1] == x1 * a[1] + x2 *b[1]:
        return x1, x2
    else:
        return 0, 0


ex = AdventOfCode(13)
ex.executeTest(part1,480)

ex.execute(part1, part2)
