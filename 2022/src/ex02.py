from AdventOfCode import AdventOfCode

score = {'R':1, 'P':2, 'S':3}
codes = {'A':'R', 'B':'P', 'C':'S','X':'R', 'Y':'P', 'Z':'S'}

winningHands = [('R','S'),('P','R'),('S','P')]

def part1(data: list):
    return sum([playHand(codes[line[0]],codes[line[2]]) for line in data])

def part2(data: list):
    return sum([playHand(codes[line[0]], handToPlay(codes[line[0]],line[2])) for line in data])

def playHand(opponent,you):
    return score[you]+roundScore(opponent,you)

def roundScore(opponent,you):
    return {2: 0, 1: 6, 0: 3}[getWinner(you, opponent)]

def getWinner(p1,p2):
    if p1 == p2:
        return 0
    elif (p1,p2) in winningHands:
        return 1
    elif (p2,p1) in winningHands:
        return 2
    else :
        raise Exception(f"invalid input: (p1,p2) = ({p1},{p2})")

def handToPlay(opponent, wantedResult):
    if wantedResult == 'Y': #draw
        return opponent
    elif wantedResult == 'X': #must lose
        for hand in winningHands:
            if(hand[0] == opponent): return hand[1]
    elif wantedResult == 'Z':
        for hand in winningHands:
            if(hand[1] == opponent): return hand[0]
    else :
        raise Exception(f"Unexpected input {opponent} {wantedResult}")


ac = AdventOfCode(2)
ac.executeTest(part1)
ac.executeTest(part2)

ac.execute(part1,part2)