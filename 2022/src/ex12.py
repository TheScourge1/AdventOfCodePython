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
    steps_done = [[-1 for column in range(width)] for row in range(height)]
    steps_done[matrix.start_location[0]][matrix.start_location[1]] = 0

    for steps in range(0, height*width + 1):
        target_reached = do_one_step(matrix, steps, steps_done)
        if target_reached:
            return steps + 1


def part2(data: list[str]):
    matrix = load_grid(data)
    width = len(matrix.grid[0])
    height = len(matrix.grid)
    steps_done = [[-1 for column in range(width)] for row in range(height)]
    steps_done[matrix.end_location[0]][matrix.end_location[1]] = 0

    for steps in range(0, height*width + 1):
        target_reached = one_step_back(matrix, steps, steps_done)
        if target_reached:
            return steps + 1


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


def do_one_step(matrix: Matrix, steps_done:int, steps_to_reach:  list[list[int]]) -> bool:
    for row in range(0,len(steps_to_reach)):
        for col in range(0,len(steps_to_reach[0])):
            if steps_to_reach[row][col] == steps_done:
                for new_row in range(max(0, row - 1), min(len(matrix.grid), row + 2)):
                    for new_col in range(max(0, col - 1), min(len(matrix.grid[0]), col + 2)):
                        if (   # only diagonal
                                (new_row == row or new_col == col) and
                                # only continue if no better path to this location allready exists
                                (steps_to_reach[new_row][new_col] == -1 or steps_to_reach[new_row][new_col] > steps_done) and
                                # no more then one lower per move
                                matrix.grid[new_row][new_col] - matrix.grid[row][col] <= 1):

                            steps_to_reach[new_row][new_col] = steps_done+1
                            if (new_row, new_col) == matrix.end_location:
                                return True

    return False


def one_step_back(matrix: Matrix, steps_done:int, steps_to_reach:  list[list[int]]) -> bool:
    for row in range(0,len(steps_to_reach)):
        for col in range(0,len(steps_to_reach[0])):
            if steps_to_reach[row][col] == steps_done:
                for new_row in range(max(0, row - 1), min(len(matrix.grid), row + 2)):
                    for new_col in range(max(0, col - 1), min(len(matrix.grid[0]), col + 2)):
                        if (   # only diagonal
                                (new_row == row or new_col == col) and
                                # only continue if no better path to this location allready exists
                                (steps_to_reach[new_row][new_col] == -1 or steps_to_reach[new_row][new_col] > steps_done) and
                                # no more then one lower per move
                                matrix.grid[row][col] - matrix.grid[new_row][new_col] <= 1):

                            steps_to_reach[new_row][new_col] = steps_done+1
                            if matrix.grid[new_row][new_col] == matrix.grid[matrix.start_location[0]][matrix.start_location[1]]:
                                return True


    return False


def print_visited(matrix):
    for i in range(0, len(matrix)):
        s = ""
        for j in range(0, len(matrix[0])):
            if(matrix[i][j]>=0):
                s+= str(matrix[i][j]) + '\t'
            else:
                s+= '.\t'
        print(s)
    print("\n")


ex12 = AdventOfCode(12)

ex12.executeTest(part1, 31)
ex12.executeTest(part2, 29)

ex12.execute(part1, part2)