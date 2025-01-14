from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    orders, sequences = read_data(data)

    return sum([get_mid(s) for s in sequences if is_correct_order(s,orders)])


def part2(data: list):
    orders, sequences = read_data(data)
    sorted_sequences = [sort_sequence(s, orders) for s in sequences if not is_correct_order(s, orders)]
    return sum([get_mid(s) for s in sorted_sequences])


def read_data(data: list[str]) -> (dict[int, list[int]], list[int]):
    orders = {}
    sequences = []
    for line in data:
        line = line.strip()
        if line.count("|") > 0:
            read_order(line, orders)
        elif line.count(",") > 0:
            sequences.append(list(map(int,line.split(","))))
    return orders,sequences


def get_mid(s:list[int]) -> int:
    return s[int((len(s)-1)/2)]


def read_order(line: str, orders: dict[int, list[int]]) -> dict[int, list[int]]:
    order = list(map(int, line.split("|")))
    orders.setdefault(order[0], []).append(order[1])
    return orders


def is_correct_order(sequence: list,orders: dict[int,list[int]]) -> bool:
    for i in range(0, len(sequence)):
        if sequence[i] in orders.keys() and len(set(orders[sequence[i]]).intersection(set(sequence[:i+1]))) > 0:
            return False
    return True


def sort_sequence(sequence: list[int], orders: dict[int,list[int]]) -> list[int]:
    result = []
    for s in sequence:
        if s in orders.keys():
            for r in result:
                if r in orders[s]:
                    result.insert(result.index(r), s)
                    break

        if s not in result:
            result.append(s)
    return result


ex = AdventOfCode(5)
ex.executeTest(part1,143)
ex.executeTest(part2,123)

ex.execute(part1, part2)
