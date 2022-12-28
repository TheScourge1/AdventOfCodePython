from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import sys


@dataclass
class Matrix:
    grid: list[list[int]]
    start_location: tuple[int,int]
    end_location: tuple[int,int]

    def __init__(self, grid, start_location, end_location):
        self.grid = grid
        self.start_location = start_location
        self.end_location = end_location


def part1(data: list[str]):
    matrix = load_grid(data)
    width = len(matrix.grid[0])
    height = len(matrix.grid)
    min_steps = [[0 for column in range(width)] for row in range(height)]
    result = traverse_grid(matrix, min_steps, [matrix.start_location], height*width + 1)

    return result


def part2(data: list[str]):
    matrix = load_grid(data)
    width = len(matrix.grid[0])
    height = len(matrix.grid)
    min_steps = [[0 for column in range(width)] for row in range(height)]
    result = inverse_lookup(matrix,min_steps, [matrix.end_location],height*width + 1)

    return result


def load_grid(data: list[str]) -> Matrix:
    array: list[list[int]] = []
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)

    for line in data:
        row: list[int] = []
        array.append(row)
        for s in line.strip():
            if s == 'S':
                start = (len(array)-1, len(row))
                row.append(0)
            elif s == 'E':
                end = (len(array)-1, len(row))
                row.append(ord('z')-ord('a'))
            else:
                row.append(ord(s)-ord('a'))
    result = Matrix(array, start, end)
    return result


def traverse_grid(matrix: Matrix, min_steps: list[list[int]], path: list[tuple[int, int]], best_result,) -> int:
    current_location = path[len(path)-1]
    if current_location == matrix.end_location:
        return len(path) - 1

    row_range = (max(0, current_location[0]-1), min(len(matrix.grid)-1, current_location[0]+1))
    col_range = (max(0, current_location[1] - 1),min(len(matrix.grid[0])-1, current_location[1] + 1))
    result = best_result

    for i in range(row_range[0], row_range[1]+1):
        for j in range(col_range[0], col_range[1]+1):
            new_loc = (i, j)

            if ((   # only diagonal
                    new_loc[0] == current_location[0] or new_loc[1] == current_location[1]) and
                    # only continue if no better path to this location allready exists
                    (min_steps[new_loc[0]][new_loc[1]] == 0 or min_steps[new_loc[0]][new_loc[1]] > len(path)+1) and
                    #check allready visited
                     new_loc not in path and
                    # no more then one higher per move
                    matrix.grid[new_loc[0]][new_loc[1]] - matrix.grid[current_location[0]][current_location[1]] <= 1
                ):

                new_path = path.copy()
                new_path.append(new_loc)
                min_steps[new_loc[0]][new_loc[1]] = len(new_path)
                new_result = traverse_grid(matrix, min_steps, new_path, result)
                if new_result < result:
                    result = new_result

    return result


def inverse_lookup(matrix: Matrix, min_steps: list[list[int]], path: list[tuple[int, int]], best_result) -> int:
    current_location = path[len(path)-1]
    if matrix.grid[current_location[0]][current_location[1] == 0]:
        return len(path) - 1

    row_range = (max(0, current_location[0]-1), min(len(matrix.grid)-1, current_location[0]+1))
    col_range = (max(0, current_location[1] - 1),min(len(matrix.grid[0])-1, current_location[1] + 1))
    result = best_result

    for i in range(row_range[0], row_range[1]+1):
        for j in range(col_range[0], col_range[1]+1):
            new_loc = (i, j)

            if ((   # only diagonal
                    new_loc[0] == current_location[0] or new_loc[1] == current_location[1]) and
                    # only continue if no better path to this location allready exists
                    (min_steps[new_loc[0]][new_loc[1]] == 0 or min_steps[new_loc[0]][new_loc[1]] > len(path)+1) and
                    #check allready visited
                     new_loc not in path and
                    # no more then one lower per move
                    matrix.grid[current_location[0]][current_location[1]] - matrix.grid[new_loc[0]][new_loc[1]] <= 1
                ):

                new_path = path.copy()
                new_path.append(new_loc)
                min_steps[new_loc[0]][new_loc[1]] = len(new_path)
                new_result = inverse_lookup(matrix, min_steps, new_path, result)
                if new_result < result:
                    result = new_result

    return result


def print_visited(matrix):
    for i in range(0, len(matrix)):
        s = ""
        for j in range(0, len(matrix[0])):
            if(matrix[i][j]>0):
                s+= str(matrix[i][j]) + '\t'
            else:
                s+= '.\t'
        print(s)


ex12 = AdventOfCode(12)
sys.setrecursionlimit(5000)
ex12.executeTest(part1, 31)
ex12.executeTest(part2, 29)

ex12.execute(part1, part2)