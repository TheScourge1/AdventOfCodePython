from AdventOfCode import AdventOfCode

def part1(data):
    line = data[0]
    return findMarkerForSize(line, 4)


def part2(data):
    line = data[0]
    return findMarkerForSize(line, 14)

def findMarkerForSize(line, size):
    for i in range(4, len(line)):
        if len(set(line[i-size:i])) == size:
            return i
    return -1


ex06 = AdventOfCode(6)
ex06.executeTest(part1, 7)
ex06.executeTest(part2, 19)

ex06.execute(part1, part2)
