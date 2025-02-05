from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    initial_list = list(map(int, data[0].strip().split(" ")))
    result = initial_list
    for i in range(0, 25):
        result = blink(result)

    return len(result)


def part2(data:list[str]):
    initial_list = list(map(int, data[0].strip().split(" ")))
    cache = {}

    return sum([depth_first(val,cache,0,75) for val in initial_list])


def depth_first(lst:int, cache: dict[(int,int), int],cur_depth: int, max_depth: int) -> int:
    if cur_depth == max_depth:
        return 1
    result = 0
    next_vals = blink([lst])
    for val in next_vals:
        if (val, cur_depth+1) in cache.keys():
            result += cache[(val,cur_depth+1)]
        else:
            res = depth_first(val,cache,cur_depth+1, max_depth)
            cache[(val, cur_depth+1)] = res
            result += res
    return result


def blink(lst: list[int]) -> list[int]:
    result = []
    for stone in lst:
        if stone == 0:
            result.append(1)
        elif len(str(stone)) % 2 == 0:
            size = len(str(stone))//2
            result.append(int(str(stone)[:size]))
            result.append(int(str(stone)[size:]))
        else:
            result.append(stone*2024)
    return result


ex = AdventOfCode(11)
ex.executeTest(part1, 55312)

ex.execute(part1, part2)