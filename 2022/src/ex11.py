from AdventOfCode import AdventOfCode
from dataclasses import dataclass,field
import math
import re


@dataclass
class Monkey:
    id: int = -1
    items: list[int] = field(default_factory=list)
    operation: (str, str, str) = ('x', 'x', 'x') #eg: ('old','*','19')
    test_value: int = -1
    true_monkey_id: int = -1
    false_monkey_id: int = -1

    def inspect_worry_level(self, item: int) -> int:
        a = item if self.operation[0] == 'old' else int(self.operation[0])
        b = item if self.operation[2] == 'old' else int(self.operation[2])
        if self.operation[1] == '+':
            return a + b
        elif self.operation[1] == "*":
            return a * b
        else:
            raise Exception(f"unknown operation: {self.operation}")


def part1(data: list[str]) -> int:
    monkeys = load_data(data)
    inspect_count = [0]*len(monkeys)
    for i in range(0, 20):
        for monkey in monkeys:
            for item in monkey.items:
                new_worry_level = monkey.inspect_worry_level(item)
                new_worry_level = math.floor(new_worry_level/3)
                inspect_count[monkey.id] += 1
                if new_worry_level % monkey.test_value == 0:
                    monkeys[monkey.true_monkey_id].items.append(new_worry_level)
                else:
                    monkeys[monkey.false_monkey_id].items.append(new_worry_level)
            monkey.items.clear()
    inspect_count = sorted(inspect_count, reverse=True)
    return inspect_count[0]*inspect_count[1]


def part2(data: [str]) -> int:
    monkeys = load_data(data)
    inspect_count = [0] * len(monkeys)
    upper_limit = 1
    for monkey in monkeys:
        upper_limit *= monkey.test_value

    for i in range(0, 10000):
        for monkey in monkeys:
            for item in monkey.items:
                new_worry_level = monkey.inspect_worry_level(item)
                new_worry_level = math.floor(new_worry_level) % upper_limit
                inspect_count[monkey.id] += 1
                if new_worry_level % monkey.test_value == 0:
                    monkeys[monkey.true_monkey_id].items.append(new_worry_level)
                else:
                    monkeys[monkey.false_monkey_id].items.append(new_worry_level)
            monkey.items.clear()
    inspect_count = sorted(inspect_count, reverse=True)
    return inspect_count[0] * inspect_count[1]


def load_data(data: [str]) -> [Monkey]:
    result :[Monkey] = []
    current_monkey = None
    for line in data:
        m = re.match("Monkey (\d+)",line)
        if m:
            current_monkey = Monkey()
            current_monkey.id = int(m.group(1))
            result.append(current_monkey)
        m = re.match("\s+Starting items: ([0-9, ]+)",line)
        if m:
            current_monkey.items = [ int(item) for item in m.group(1).split(', ')]
        m = re.match("\s+Operation: new = ([a-z0-9]+) ([*+]) ([a-z0-9]+)",line)
        if m:
            current_monkey.operation = (m.group(1), m.group(2), m.group(3))
        m = re.match("\s+Test: divisible by (\d+)",line)
        if m:
            current_monkey.test_value = int(m.group(1))
        m = re.match("\s+If true: throw to monkey (\d+)",line)
        if m:
            current_monkey.true_monkey_id = int(m.group(1))
        m = re.match("\s+If false: throw to monkey (\d+)", line)
        if m:
            current_monkey.false_monkey_id = int(m.group(1))
    return result


ex11 = AdventOfCode(11)

ex11.executeTest(part1, 10605)
ex11.executeTest(part2, 2713310158)

ex11.execute(part1, part2)
