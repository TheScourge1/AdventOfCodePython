from AdventOfCode import AdventOfCode
import math

def part1(data):
    tree_grid = get_tree_grid(data)
    visible_grid = [[False]*len(tree_grid[0]) for j in range(len(tree_grid))]

    for i in range(0, len(tree_grid)):
        for j in range(0, len(tree_grid[0])):
            if i == 0 or j == 0 or i == len(tree_grid)-1 or j == len(tree_grid[0])-1:
                visible_grid[i][j]=True

    for i in range(0, len(tree_grid)):
        max_height_left = tree_grid[i][0]
        max_height_right = tree_grid[i][len(tree_grid[0])-1]
        for j in range(1, len(tree_grid[0])):
            if tree_grid[i][j] > max_height_left:
                visible_grid[i][j]=True
                max_height_left = tree_grid[i][j]
            if tree_grid[i][len(tree_grid[0])-j] > max_height_right:
                visible_grid[i][len(tree_grid[0])-j] = True
                max_height_right = tree_grid[i][len(tree_grid[0])-j]

    for j in range(0, len(tree_grid[0])):
        max_height_top = tree_grid[0][j]
        max_height_bottom = tree_grid[len(tree_grid)-1][j]
        for i in range(1, len(tree_grid)):
            if tree_grid[i][j] > max_height_top:
                visible_grid[i][j]=True
                max_height_top = tree_grid[i][j]
            if tree_grid[len(tree_grid)-i][j] > max_height_bottom:
                visible_grid[len(tree_grid)-i][j] = True
                max_height_bottom = tree_grid[len(tree_grid)-i][j]

    return sum([sum([1 for element in row if element]) for row in visible_grid])


def get_tree_grid(data):
    result = []
    for line in data:
        result.append([int(s) for s in line.strip()])
    return result


def part2(data):
    tree_grid = get_tree_grid(data)
    scenic_score = 0
    for i in range(0,len(tree_grid)):
        for j in range(0,len(tree_grid[0])):
            current_score = get_scenic_score(tree_grid,i,j)
            if scenic_score < current_score:
                scenic_score = current_score
    return scenic_score

def get_scenic_score(grid,i,j):
    max_i = len(grid)
    max_j = len(grid[0])
    result = [0]*4
    for a in range(i+1,max_i):
        result[0] += 1
        if grid[i][j] <= grid[a][j]:
            break

    for a in range(i-1,-1,-1):
        result[1] += 1
        if grid[i][j] <= grid[a][j]:
            break

    for a in range(j + 1, max_j):
        result[2] += 1
        if grid[i][j] <= grid[i][a]:
            break

    for a in range(j - 1, -1, -1):
        result[3] += 1
        if grid[i][j] <= grid[i][a]:
            break

    return math.prod(result)


ex08 = AdventOfCode(8)

ex08.executeTest(part1, 21)
ex08.executeTest(part2, 8)

ex08.execute(part1, part2)
