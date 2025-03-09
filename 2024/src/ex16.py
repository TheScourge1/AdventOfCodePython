from AdventOfCode import AdventOfCode

from dataclasses import dataclass


ROTATE = {0: (0, -1), 90: (1, 0), 180: (0, 1), 270: (-1, 0)}

@dataclass(frozen=True)
class Cursor:
    p: (int, int)
    deg: int

    def move_right(self) -> 'Cursor':
        v = (self.deg + 90) % 360
        return Cursor((self.p[0]+ROTATE[v][0], self.p[1]+ROTATE[v][1]), v)

    def move_left(self) -> 'Cursor':
        v = (360 + self.deg - 90) % 360
        return Cursor((self.p[0]+ROTATE[v][0], self.p[1]+ROTATE[v][1]), v)

    def move(self) -> 'Cursor':
        return Cursor((self.p[0]+ROTATE[self.deg][0], self.p[1]+ROTATE[self.deg][1]), self.deg)


def part1(data: list[str]):
    maze = [list(d.strip()) for d in data]
    start = (1, len(maze)-2)
    depth = 100
    while True:
        depth += 1
        cost_matrix = [[0]*len(maze[0]) for line in maze]
        path_cost = [[0]*len(maze[0]) for line in maze]
        result = walk_maze(maze, Cursor(start, 90), depth, 0, cost_matrix,path_cost)
        print("depth: "+str(depth))
        if result > 0:
            return result


def part2(data: list[str]):
    maze = [list(d.strip()) for d in data]
    start = (1, len(maze)-2)
    depth = 100
    while True:
        depth += 1
        cost_matrix = [[0]*len(maze[0]) for line in maze]
        path_cost = [[0]*len(maze[0]) for line in maze]
        result = walk_maze(maze, Cursor(start, 90), depth, 0, cost_matrix,path_cost)
        if result > 0:
            return sum([line.count(result) for line in path_cost])


def walk_maze(maze: list[list[str]], cursor: Cursor, depth: int, current_cost, costs: list[list[int]], path_cost) -> int:
    if maze[cursor.p[1]][cursor.p[0]] == "E":
        costs[cursor.p[1]][cursor.p[0]] = current_cost
        path_cost[cursor.p[1]][cursor.p[0]] = current_cost
        return current_cost
    elif maze[cursor.p[1]][cursor.p[0]] == "#" or depth == 0:
        return -1
    elif 0 < costs[cursor.p[1]][cursor.p[0]] < current_cost - 1000:
         return -1
    else:
        costs[cursor.p[1]][cursor.p[0]] = current_cost
        res1 = walk_maze(maze, cursor.move(), depth, current_cost + 1, costs, path_cost)
        res2 = walk_maze(maze, cursor.move_left(), depth - 1, current_cost + 1001, costs, path_cost)
        res3 = walk_maze(maze, cursor.move_right(), depth - 1, current_cost + 1001, costs, path_cost)
        results = {res1, res2, res3}
        results.remove(-1)
        if len(results) == 0:
            return -1
        path_cost[cursor.p[1]][cursor.p[0]] = min(results)
        return min(results)


def print_maze(maze: list[list[str]]):
    for row in maze:
        line = "".join(row)
        print(line)


def print_cost(maze: list[list[int]]):
    for row in maze:
        line = "".join([str(s % 1000)+"\t" for s in row])
        print(line)


ex = AdventOfCode(16)
ex.executeTest(part1, 11048)
ex.executeTest(part2, 64)

ex.execute(part1, part2)