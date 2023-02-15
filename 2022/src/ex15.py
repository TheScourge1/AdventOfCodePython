from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import re


@dataclass
class Sensor:
    x: int
    y: int

    beacon_x: int
    beacon_y: int


def part1(data: list[str]) -> int:
    sensors = read_data(data)
    y_check = 10
    if len(data) > 15:
        y_check = 2000000

    ranges = get_coverage_at_line(y_check, sensors)
    distinct_ranges = merge_ranges(ranges)

    return sum([r[1]-r[0] for r in distinct_ranges])


def part2(data: list[str]) -> str:
    sensors = read_data(data)
    max_range = 20
    if len(data) > 15:
        max_range = 4000000

    for y in range(0, max_range+1):
        ranges = get_coverage_at_line(y, sensors)
        distinct_ranges = merge_ranges(ranges)
        if len(distinct_ranges) > 1:
            return (distinct_ranges[0][1]+1)*4000000+y

    return "not found"

def get_coverage_at_line(line: int, sensors: list[Sensor]) -> list[tuple[int, int]]:
    ranges = []
    for sensor in sensors:
        distance = abs(sensor.x - sensor.beacon_x) + abs(sensor.y - sensor.beacon_y)
        delta_x = distance - abs(sensor.y - line)
        if delta_x > 0:
            delta = (sensor.x-delta_x, sensor.x+delta_x)
            ranges.append((min(delta[0], delta[1]), max(delta[0], delta[1])))
    return ranges


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges = sorted(ranges, key=lambda r: r[0])
    current_range = ranges[0]
    distinct_ranges = []

    for range in ranges[1:]:
        if current_range[0] <= range[0] <= current_range[1]:
            if range[1] > current_range[1]:
                current_range = (current_range[0], range[1])
        else:
            distinct_ranges.append(current_range)
            current_range = range
    distinct_ranges.append(current_range)
    return distinct_ranges


def read_data(data: list[str]) -> list[Sensor]:
    result = []
    for line in data:
        res = re.findall(r'(\d+)', line)
        result.append(Sensor(x=int(res[0]), y=int(res[1]), beacon_x=int(res[2]), beacon_y=int(res[3])))

    return result


ex15 = AdventOfCode(15)
ex15.executeTest(part1, 26)
ex15.executeTest(part2, 56000011)

ex15.execute(part1, part2)
