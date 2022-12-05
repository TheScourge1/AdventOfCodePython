from AdventOfCode import AdventOfCode

def part1(data: list):
    calories = getCaloryList(data)
    return sorted(calories,reverse=True)[0]

def part2(data: list):
    calories = getCaloryList(data)
    topThree = sorted(calories,reverse=True)[0:3]
    return sum(topThree)

def getCaloryList(data:list):
    calories = []
    currentCalories = 0
    for calory in data:
        if calory == "":
            calories.append(currentCalories)
            currentCalories = 0
        else:
            currentCalories += int(calory)
    calories.append(currentCalories)
    return calories


ex = AdventOfCode(1)
ex.executeTest(part1)
ex.executeTest(part2)

ex.execute(part1,part2)