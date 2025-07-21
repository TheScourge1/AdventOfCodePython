from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    secrets: list[int] = [int(s) for s in data]
    result = 0
    for sec in secrets:
        temp = sec
        for _ in range(2000):
            temp = do_round(temp)
        result += temp
    return result


def part2(data: list[str]):
    secrets: list[int] = [int(s) for s in data]
    diff_list = []
    for sec in secrets:
        temp = sec
        costs = []
        diffs: dict[str, int] = {}
        for i in range(2000):
            temp = do_round(temp)
            costs.append(temp % 10)
            if i >= 4:
                diff = f"{(costs[i-4]-costs[i-3])}{(costs[i-3]-costs[i-2])}{(costs[i-2]-costs[i-1])}{(costs[i-1]-costs[i])}"
                if diffs.get(diff) is None:
                    diffs[diff] = costs[i]
        diff_list.append(diffs)
    return max_diff(diff_list)


def do_round(secret: int) -> int:
    result = prune(mix(secret, secret * 64))
    result = prune(mix(result, result >> 5))
    result = prune(mix(result, result * 2048))
    return result


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int) -> int:
    return a % 16777216


def max_diff(data: list[dict[str, int]]) -> int:
    diffs = set([])
    for d in data:
        diffs = diffs.union(d.keys())
    result = 0
    for diff in diffs:
        temp = sum([d.get(diff, 0) for d in data])
        if temp > result:
            result = temp
    return result


ex = AdventOfCode(22)
ex.executeTest(part1, 37327623)

ex.execute(part1, part2)
