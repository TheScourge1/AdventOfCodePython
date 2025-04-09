from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    towels, patterns = read_data(data)
    return sum([1 for p in patterns if is_valid_pattern(p, towels)])


def part2(data: list[str]):
    towels, patterns = read_data(data)
    return sum([count_combinations(p, towels,{}) for p in patterns])


def is_valid_pattern(pattern: str, towels: list[str]) -> bool:
    for t in towels:
        if pattern == t or (pattern.startswith(t) and is_valid_pattern(pattern[len(t):], towels)):
            return True
    return False


def count_combinations(pattern: str, towels: list[str], cache: dict[str,int]) -> int:
    if pattern in cache.keys():
        return cache[pattern]

    result = 0
    for t in towels:
        if pattern == t:
            result += 1
        if pattern.startswith(t):
            result += count_combinations(pattern[len(t):], towels, cache)
    cache[pattern] = result

    return result


def read_data(data: list[str]) -> (list[str], list[str]):
    towels = list(data[0].strip().split(", "))
    patterns = [line.strip() for line in data[2:]]
    return towels, patterns


ex = AdventOfCode(19)
ex.executeTest(part1, 6)
ex.executeTest(part2, 16)

ex.execute(part1, part2)
