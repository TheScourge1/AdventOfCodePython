from AdventOfCode import AdventOfCode
import numpy as np

WORDS = ["XMAS","SAMX"]
WORDS2 = ["MAX","XAM"]

INDEXES = [[(0,0),(0,1),(0,2),(0,3)],[(0,0),(1,0),(2,0),(3,0)],[(0,0),(1,1),(2,2),(3,3)],[(0,3),(1,2),(2,1),(3,0)]]
INDEXES2 = [[(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)]]

def part1(data: list):
    grid = np.array([list(line.strip()) for line in data])
    return search(grid)


def part2(data: list):
    grid = np.array([list(line.strip()) for line in data])
    return search2(grid)


def search(grid) -> int:
    result = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            for ind in INDEXES:
                word = get_index_word(grid,(i,j),ind)
                if(WORDS.count(word)) > 0:
                        result += 1
    return result


def search2(grid) -> int:
    result = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            word1 = get_index_word(grid,(i,j),INDEXES2[0])
            word2 = get_index_word(grid,(i,j),INDEXES2[1])
            if WORDS2.count(word1) > 0 and WORDS2.count(word2) > 0:
                result += 1
    return result


def get_index_word(grid,loc,indexes:list) -> str:
    if max([loc[0]+indexes[i][0] for i in range(0, len(indexes))]) >= len(grid):
        return "ERROR"
    if max([loc[1]+indexes[i][1] for i in range(0, len(indexes))]) >= len(grid):
        return "ERROR"

    return ''.join([grid[loc[0]+indexes[i][0]][loc[1]+indexes[i][1]] for i in range(0,len(indexes))])



ex = AdventOfCode(4)
ex.executeTest(part1,18)
ex.executeTest(part2,9)

ex.execute(part1, part2)
