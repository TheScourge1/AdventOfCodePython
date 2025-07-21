from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    comps = get_linked_objects(data)
    triplets = find_triplets(comps)
    return sum([1 for t in triplets if contains_t(t)])


def part2(data: list[str]):
    comps = get_linked_objects(data)
    combined_sets = find_triplets(comps)
    while len(combined_sets) > 1:
        new_sets = set()

        for c in combined_sets:
            for k in comps.keys():
                if is_connected(comps, c, k):
                    new_sets.add(tuple(sorted(set(c) | {k})))
        combined_sets = new_sets

    return ",".join(combined_sets.pop())


def get_linked_objects(data: list[str]) -> dict[str, set[str]]:
    data1 = [d.strip().split("-") for d in data]
    result = {}
    for d in data1:
        result.setdefault(d[0], set([])).add(d[1])
        result.setdefault(d[1], set([])).add(d[0])
    return result


def find_triplets(data: dict[str, set[str]]) -> set[tuple[str, str, str]]:
    result = set([])
    for d in data.keys():
        for e in data[d]:
            for f in data[d]:
                if d != e and d != f and e != f and is_triplet(data,(d, e, f)):
                    result.add(tuple(sorted((d, e, f))))
    return result


def is_triplet(data: dict[str, set[str]], t: tuple[str, str, str]) -> bool:
    if t[1] in data[t[0]] and t[2] in data[t[0]] and t[2] in data[t[1]]:
        return True
    return False


def is_connected(data: dict[str, tuple[str]], pool: set[str], new_val: str) -> bool:
    for p in pool:
        if p not in data[new_val]:
            return False
    return True


def contains_t(t: tuple[str, str, str]) -> bool:
    return True if t[0][0] == 't' or t[1][0] == 't' or t[2][0] == 't' else False


ex = AdventOfCode(23)
ex.executeTest(part1, 7)
ex.executeTest(part2, 'co,de,ka,ta')

ex.execute(part1, part2)
