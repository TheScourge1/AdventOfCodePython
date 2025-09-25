import numpy as np
from AdventOfCode import AdventOfCode
from dataclasses import dataclass, field

@dataclass
class TestInput:
    keys: list[list[int]] = field(default_factory=list)
    locs: list[list[int]] = field(default_factory=list)

    def add_item(self, item: list[list[str]]):
        transposed = np.array(item[1:-1]).T
        cnt_list = [np.sum(c == "#") for c in transposed]
        if item[0].count("#") == 5:
            self.locs.append(cnt_list)
        else:
            self.keys.append(cnt_list)


def part1(data:list[str]):
    input_data = read_data(data)

    result = 0
    for loc in input_data.locs:
        for key in input_data.keys:
           if len([s for s in (np.array(loc) + np.array(key)) if s > 5]) == 0:
              result += 1
    return result


def part2(data: list[str]):
    pass


def read_data(data:list[str]) -> TestInput:
    result = TestInput()
    current_read = []
    for line in data:
        line = line.strip()
        if len(line) == 0:
            result.add_item(current_read)
            current_read = []
        else:
            current_read.append(list(line))
        if len(current_read) > 7:
            raise Exception(f"Unexpected matrix size read: {current_read}")

    if len(current_read) == 7:
        result.add_item(current_read)
    else:
        raise Exception(f"Unexpected last matrix size read: {current_read}")
    return result


ex = AdventOfCode(25)
ex.executeTest(part1,3)

ex.execute(part1, part2)