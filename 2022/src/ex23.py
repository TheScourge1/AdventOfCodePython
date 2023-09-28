from AdventOfCode import AdventOfCode


MOVES = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
ADJACENT_POSITIONS = {'N': [(-1,-1),(-1, 0),(-1,1)],
                      'S': [(1,-1),(1, 0),(1,1)],
                      'W': [(-1, -1),(0, -1),(1, -1)],
                      'E': [(-1, 1),(0, 1),(1, 1)]}
MOVES_ORDER = ['N', 'S', 'W', 'E']

def part1(data: list[str]) -> str:
    grid: list[list[str]] = read_start_grid(data)
    print_datagrid(grid)

    for i in range(0, 10):
        grid = move_round(grid, i % len(MOVES_ORDER))

    return str(count_ground_tiles(grid))


def part2(data: str) -> str:
    grid: list[list[str]] = read_start_grid(data)

    for i in range(0, 10000):
        new_grid = move_round(grid, i % len(MOVES_ORDER))

        if compare_grids(grid, new_grid):
            return str(i+1)
        grid = new_grid


def move_round(input_grid: list[list[str]], first_direction:int) -> list[list[str]]:
    input_grid = expand_grid(input_grid)
    proposal_grid = propose_moves(input_grid, first_direction)
    result = execute_moves(input_grid, proposal_grid, first_direction)
    return result


def propose_moves(input_grid: list[list[str]],first_direction:int) -> list[list[int]]:
    proposed_moves_grid = [[0 for _ in range(len(input_grid[0]))] for _ in range(len(input_grid))]
    for y in range(1,len(input_grid)-1):
        for x in range(1,len(input_grid[0])-1):
            if input_grid[y][x] == "#":
                move = get_move(input_grid,first_direction,(y,x))
                proposed_moves_grid[move[0]][move[1]] += 1
    return proposed_moves_grid


def execute_moves(input_grid: list[list[str]],proposal_grid, first_direction:int) -> list[list[str]]:
    target_grid = [["." for _ in range(len(input_grid[0]))] for _ in range(len(input_grid))]
    for y in range(1,len(input_grid)-1):
        for x in range(1,len(input_grid[0])-1):
            if input_grid[y][x] == "#":
                move = get_move(input_grid,first_direction,(y,x))
                match proposal_grid[move[0]][move[1]]:
                    case 0:
                        raise Exception(f"Unexpected move {move}")
                    case 1:
                        target_grid[move[0]][move[1]] = "#"
                    case _:
                        target_grid[y][x] = "#"

    return target_grid


def get_move(input_grid: list[list[str]], first_direction:int, location: tuple[int,int]) -> tuple[int,int]:
    has_heighbour = False
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if input_grid[location[0]+i][location[1]+j] == "#" and (i != 0 or j != 0):
                has_heighbour = True
    if not has_heighbour:
        return location

    for i in range(0, len(MOVES)):
        target_free = True
        move = MOVES_ORDER[(first_direction+i)%len(MOVES)]
        for delta in ADJACENT_POSITIONS[move]:
            if input_grid[location[0]+delta[0]][location[1]+delta[1]] == "#":
                target_free = False
        if target_free:
            return location[0]+MOVES[move][0],location[1]+MOVES[move][1]

    return location



def expand_grid(input_grid:list[list[str]]) -> list[list[str]]:
    result = []
    if "#" in input_grid[0]:
        result.append(list("."*len(input_grid[0])))
    result.extend(input_grid)
    if "#" in input_grid[len(input_grid)-1]:
        result.append(list("."*len(input_grid[0])))
    add_first_row = False
    add_last_row = False
    for row in result:
        if row[0] == "#":
            add_first_row = True
        if row[len(row)-1] == "#":
            add_last_row = True
    result2 = []
    for row in result:
        new_row = []
        if add_first_row:
            new_row.append(".")
        new_row.extend(row)
        if add_last_row:
            new_row.append(".")
        result2.append(new_row)

    return result2


def count_ground_tiles(input_grid: list[list[str]]) -> int:
    min_x = 1
    min_y = 1
    max_y = len(input_grid)-2
    max_x = len(input_grid[0])-2
    for y in range(0,len(input_grid)):
        for x in range(0,len(input_grid[0])):
            if input_grid[y][x] == "#":
                if y < min_y:
                    min_y = y
                elif y > max_y:
                    max_y = y
                if x < min_x:
                    min_x = x
                elif x > max_x:
                    max_x = x
    result = 0
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            if input_grid[y][x] == ".":
                result+=1
    return result


def print_datagrid(grid: list[list[str]]):
    for i in range(0,len(grid)):
        line = ""
        for j in range(0,len(grid[0])):
            line += str(grid[i][j])
        print(line)
    print("")


def read_start_grid(data: list[str]) -> list[list[str]]:
    result = []
    for line in data:
        result.append(list(line.strip()))
    return result


def compare_grids(old_grid: list[list[str]],new_grid: list[list[str]]) -> bool:
    grid_a = old_grid
    grid_b = new_grid

    if len(old_grid)!= len(new_grid) or len(old_grid[0]) != len(new_grid[0]):
        grid_a = expand_grid(grid_a)
        grid_b = expand_grid(grid_b)

    for y in range(0,len(grid_a)):
        for x in range(0,len(grid_a[0])):
            if grid_a[y][x] != grid_b[y][x]:
                return False

    return True

ex23 = AdventOfCode(23)
ex23.executeTest(part1, "110")
ex23.executeTest(part2, "20")

ex23.execute(part1, part2)


