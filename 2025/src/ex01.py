from AdventOfCode import AdventOfCode

START_LOCATION = 50

def part1(data: list):
    location = START_LOCATION
    result = 0
    for d in data:
        sign = 1 if d[0] == 'R' else -1
        location += sign * int(d[1:])
        location %= 100
        if location == 0:
            result += 1
    return result


def part2(data: list):
    location = START_LOCATION
    result = 0
    for d in data:
        distance = int(d[1:]) if d[0] == 'R' else -int(d[1:])
        if location != 0 and location + distance <= 0:
            result += 1
        location = location + distance
        result += abs(location) // 100
        location %= 100
    return result


ex = AdventOfCode(1)
ex.executeTest(part1,3)
ex.executeTest(part2,6)

ex.execute(part1,part2)