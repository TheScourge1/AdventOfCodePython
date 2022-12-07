from AdventOfCode import AdventOfCode


def part1(data):
    result = 0
    for line in data:
        pair1, pair2 = getPairs(line)
        if (pair1[0] >= pair2[0] and pair1[1] <= pair2[1]) or (pair2[0] >= pair1[0] and pair2[1] <= pair1[1]):
            result += 1
    return result


def part2(data):
    result = 0
    for line in data:
        pair1, pair2 = getPairs(line)
        if (pair2[0] <= pair1[0] <= pair2[1] or pair2[0] <= pair1[1] <= pair2[1]
         or pair1[0] <= pair2[0] <= pair1[1] or pair1[0] <= pair2[1] <= pair1[1]):
            result += 1
    return result


def getPairs(line):
    split = [s.split("-") for s in str(line).split(",")]
    return (int(split[0][0]), int(split[0][1])), (int(split[1][0]), int(split[1][1]))

ex4 = AdventOfCode(4)

ex4.executeTest(part1, 2)
ex4.executeTest(part2, 4)

ex4.execute(part1, part2)
