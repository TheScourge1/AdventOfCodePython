from AdventOfCode import AdventOfCode
import copy

MAP_TO_INT = {'E': -2, '#': -1, '.': 0, '^': 1, '>': 10, 'v': 100, '<': 1000}
MAP_TO_STR = {value: key for key, value in MAP_TO_INT.items()}
BLIZZARD_MOVE = {1: (-1, 0), 10: (0, 1), 100: (1,0), 1000: (0, -1)}


def part1(data: list[str]) -> str:
    grid = read_grid(data)
    grid[0][1]=-2
    #print_grid(grid)

    start = (0,1)
    end = (len(grid) -1,len(grid[0]) - 2)
    return str(execute_round(grid, [start],1 , start , end)[0])


def part2(data: list[str]) -> str:
    grid = read_grid(data)
    grid[0][1] = -2

    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 2)
    trip_one = execute_round(grid, [start],1 , start , end)
    trip_two = execute_round(trip_one[1], [end],trip_one[0] , end , start)
    trip_three = execute_round(trip_two[1], [start], trip_two[0], start, end)

    return str(trip_three[0])


def execute_round(grid: list[list[int]], possible_locations: list[tuple[int,int]], depth: int,
                  start_loc:tuple[int,int],end_loc:tuple[int,int]) -> (int,list[list[int]]):
    new_grid = evolve_grid(grid)
    new_locations: set[tuple[int,int]] = {start_loc}
    #print(f"executing round: {depth} with {len(possible_locations)} options")
    #print("")

    for location in possible_locations:
        for y_step in range(-1,2):
            for x_step in range(-1,2):
                new_loc = (location[0]+y_step,location[1]+x_step)
                if new_loc[0] < 0 or (x_step != 0 and y_step != 0) or new_loc[0] == len(grid):
                    continue
                elif new_loc == end_loc:
                    return depth,grid
                elif new_grid[new_loc[0]][new_loc[1]] == 0:
                    new_locations.add(new_loc)

    return execute_round(new_grid,list(new_locations),depth+1,start_loc,end_loc)


def evolve_grid(grid: list[list[int]]) -> list[list[int]]:
    new_grid = copy.deepcopy(grid)
    for i in range(1,len(new_grid)-1):
        for j in range(1, len(new_grid[0]) - 1):
            new_grid[i][j] = 0

    for y in range(1,len(new_grid)-1):
        for x in range(1, len(new_grid[0]) - 1):
            if grid[y][x] > 0:
                for move in get_moves(grid[y][x]):
                    step = BLIZZARD_MOVE[move]
                    new_y, new_x = y+step[0], x+step[1]

                    if new_y == 0:
                        new_y = len(new_grid)-2
                    elif new_y == len(new_grid) - 1:
                        new_y = 1
                    if new_x == 0:
                        new_x = len(new_grid[0]) - 2
                    elif new_x == len(new_grid[0]) - 1:
                        new_x = 1
                    new_grid[new_y][new_x] += move

    return new_grid


def get_moves(combined_move: int) -> list[int]:
    result = []
    for i in range(4, -1, -1):
        factor = 10 ** i
        if combined_move // factor == 1:
            result.append(factor)
            combined_move = combined_move % factor
    return result


def read_grid(data: list[str]) -> list[list[int]]:
    return [[MAP_TO_INT[s] for s in line.strip()] for line in data]


def print_grid(grid: list[list[int]]):
    for row in grid:
        print("".join([MAP_TO_STR.get(r,"+") for r in row]))


ex24 = AdventOfCode(24)
ex24.executeTest(part1, "18")
ex24.executeTest(part2, "54")

ex24.execute(part1, part2)
