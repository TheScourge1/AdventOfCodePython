from AdventOfCode import AdventOfCode


def part1(data: list):
    return sum([check_report(list(map(int,report.split())),0) for report in data])


def part2(data: list):
    return sum([check_report(list(map(int,report.split())),1) for report in data])


def check_report(report: list[int], discard_count: int) -> int:
    if report[0] == report[1]:
        if discard_count == 0:
            return 0
        else:
            return check_report(report[1:],0)
    direction = int((report[0]-report[1]) / abs(report[1]-report[0]))
    for i in range(0, len(report)-1):
        diff = direction*(report[i]-report[i+1])
        if diff < 1 or diff > 3:
            if discard_count == 0:
                return 0
            elif (check_report(report[0: i]+report[i+1: len(report)],0) == 0 and
                    check_report(report[0: i+1]+report[i+2: len(report)],0) == 0 and
                    check_report(report[1:],0) == 0):
                return 0
            else:
                print(report)
                return 1
    print(report)
    return 1


ex = AdventOfCode(2)
ex.executeTest(part1, 2)
ex.executeTest(part2, 4)

ex.execute(part1, part2)
