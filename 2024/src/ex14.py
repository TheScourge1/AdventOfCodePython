from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import re

@dataclass
class Robot:
    p: (int, int)
    v: (int, int)


def part1(data: list[str]):
    robots = read_data(data)
    if len(data) < 13:
        grid_size = (11, 7)
    else:
        grid_size = (101, 103)

    locations = [get_location(r, 100, grid_size) for r in robots]
    quadrants = get_quadrant_counts(locations, grid_size)

    return quadrants[0]*quadrants[1]*quadrants[2]*quadrants[3]


def part2(data: list[str]):
    robots = read_data(data)
    grid_size = (101, 103)

    q = int(part1(data))
    min_time = 100
    result_bots = []
    for time in range(0, 10000):
        for robot in robots:
            robot.p = get_location(robot, 1, grid_size)

        new_qs = get_quadrant_counts([r.p for r in robots], grid_size)
        new_q = new_qs[0]*new_qs[1]*new_qs[2]*new_qs[3]
        if new_q < q:
            result_bots = [Robot(r.p,r.v) for r in robots]
            q = new_q
            min_time = time

    print_robots(result_bots, grid_size)
    return min_time


def read_data(data: list[str]) -> list[Robot]:
    result = []
    pattern = r"(-?\d+)"
    for line in data:
        d = list(map(int, re.findall(pattern,line)))
        result.append(Robot((d[0], d[1]), (d[2], d[3])))
    return result


def get_location(robot: Robot, time: int, grid_size: (int, int)) -> (int, int):
    x = (robot.p[0]+time * robot.v[0] + time*grid_size[0]) % grid_size[0]
    y = (robot.p[1]+time * robot.v[1] + time*grid_size[1]) % grid_size[1]

    return x, y


def get_quadrant_counts(locs: list[(int, int)], grid_size: (int, int)) -> (int, int, int, int):
    result = [0, 0, 0, 0]

    for l in locs:
        if l[0] < grid_size[0]//2 and l[1] < grid_size[1]//2:
            result[0] += 1
        elif l[0] > grid_size[0]//2 and l[1] < grid_size[1]//2:
            result[1] += 1
        elif l[0] < grid_size[0]//2 and l[1] > grid_size[1]//2:
            result[2] += 1
        elif l[0] > grid_size[0]//2 and l[1] > grid_size[1]//2:
            result[3] += 1
    return result


def print_robots(robots: list[Robot],grid_size: (int, int)):
    for y in range(0,grid_size[1]):
        line = ""
        for x in range(0, grid_size[0]):
            bots = sum([1 for r in robots if r.p == (x, y)])
            if bots > 0:
                line += str(bots)
            else:
                line += "."
        print(line)


ex = AdventOfCode(14)
ex.executeTest(part1, 12)

ex.execute(part1, part2)
