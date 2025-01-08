from AdventOfCode import AdventOfCode


def part1(data: list):
    lst1,lst2 = read_lists(data)

    lst1.sort()
    lst2.sort()
    res = [abs(t[0]-t[1]) for t in list(zip(lst1, lst2))]
    return sum(res)


def part2(data: list):
    lst1,lst2 = read_lists(data)
    res = 0
    for id in lst1:
        res += id * lst2.count(id)

    return res


def read_lists(data:list):
    lst1: list[int] = []; lst2: list[int] = []
    for line in data:
        res = line.split()
        lst1.append(int(res[0]))
        lst2.append(int(res[1]))

    return lst1,lst2


ex = AdventOfCode(1)
ex.executeTest(part1,11)
ex.executeTest(part2,31)

ex.execute(part1,part2)