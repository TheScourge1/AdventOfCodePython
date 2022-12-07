from AdventOfCode import AdventOfCode


def part1(data):
    commonItems = [getCommonItem(sack[0:int(len(sack)/2)],sack[int(len(sack)/2):]) for sack in data]
    return sum([getPriorty(item) for item in commonItems])

def getCommonItem(sack1,sack2):
    return [s for s in sack1 if s in sack2][0]

def getPriorty(item):
    if item >= 'a' and item <= 'z':
        return ord(item)-ord('a')+1
    else:
        return ord(item)-ord('A')+27

def part2(data):
    subLists = splitList(data,3)
    badges = []
    for group in subLists:
        common12 = getCommonItems(group[0],group[1])
        common23 = getCommonItems(group[1],group[2])
        badges.append(list(set(common12).intersection(common23))[0])

    return sum([getPriorty(item) for item in badges])


def splitList(data,groupSize):
    for i in range(0,len(data),groupSize):
        yield data[i:i+groupSize]

def getCommonItems(string1, string2):
    return [s for s in string1 if s in string2]


ex3 = AdventOfCode(3)

ex3.executeTest(part1)
ex3.executeTest(part2)

ex3.execute(part1,part2)