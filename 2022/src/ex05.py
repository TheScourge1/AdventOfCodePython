from AdventOfCode import AdventOfCode
import re


class Move:
    def __init__(self, source, target, number):
        self.source = source
        self.target = target
        self.number = number

    def __repr__(self):
        return f"({self.source},{self.target},{self.number})"

def part1(data):
    stackList , moves = readInput(data)

    for move in moves:
        for i in range(0,move.number):
            stackList[move.target-1].append(stackList[move.source-1].pop())

    return "".join([stackList[key][-1] for key in sorted(stackList.keys())])


def part2(data):
    stackList, moves = readInput(data)

    for move in moves:
        srcList = stackList[move.source - 1]
        stackList[move.target - 1].extend(srcList[len(srcList)-move.number:])
        del srcList[len(srcList)-move.number:]

    return "".join([stackList[key][-1] for key in sorted(stackList.keys())])

def readInput(data):
    linenr = 0
    stackItems = []
    while('[' in data[linenr]):
        stackItems.append(readStackLine(data[linenr]))
        linenr += 1
    linenr += 2
    moves = [readMove(line) for line in data[linenr:]]

    stackList = {}
    for stackline in reversed(stackItems):
        for item in stackline:
            if not item[0] in stackList.keys():
                stackList[item[0]] = []
            stackList[item[0]].append(item[1])

    return (stackList, moves)

def readStackLine(line):
        return [(int(match.span()[0]/4),match.string[match.span()[0]+1]) for match in list(re.finditer("\[\w+\]", line))]

def readMove(line):
    cnt = re.search("move \d+",line).group()[5:]
    source = re.search("from \d+",line).group()[5:]
    target = re.search("to \d+",line).group()[3:]
    return Move(int(source), int(target), int(cnt))


ex05 = AdventOfCode(5)

ex05.executeTest(part1,"CMZ")
ex05.executeTest(part2,"MCD")

ex05.execute(part1,part2)