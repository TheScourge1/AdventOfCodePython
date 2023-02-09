from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    paths = [read_line(line) for line in data]
    matrix = create_matrix(paths)

    for path in paths:
        matrix = add_path(matrix, path)

    result = 0
    while add_sanddrop(matrix):
        result += 1

    return result

def part2(data: list[str]):
    paths = [read_line(line) for line in data]
    matrix = create_matrix(paths)

    for path in paths:
        matrix = add_path(matrix, path)

    matrix = add_bottom(matrix)

    result = 0
    while add_sanddrop(matrix):
        result += 1

    return result


def read_line(line:str) -> list((int, int)):
    coords = line.strip().split(" -> ")
    return [tuple(map(int,coord.split(","))) for coord in coords]

def create_matrix(paths: list[(int,int)]) -> list[list[chr]]:
    min_x = min([coord[0] for path in paths for coord in path])-1
    max_x = max([coord[0] for path in paths for coord in path])+1
    max_y = max([coord[1] for path in paths for coord in path])

    result = []
    for i in range(0, max_y+1):
        row = ['.'] * (max_x+1-min_x+1)*8
        result.append(row)
    result[0][(max_x+1-min_x)*4] = '+'
    return result

def add_path(matrix: list[list[chr]], path: list[(int,int)]) -> list[list[chr]]:
    center_col = matrix[0].index('+')
    for i in range(0,len(path)-1):
        if(path[i][0] == path[i+1][0]):
            col = path[i][0]
            for row in range(min(path[i][1], path[i+1][1]),max(path[i][1], path[i+1][1])):
                matrix[row][col-500+center_col] = "#"
        else:
            row = path[i][1]
            for col in range(min(path[i+1][0], path[i][0]),max(path[i+1][0], path[i][0])+1):
                matrix[row][col-500+center_col] = "#"

    return matrix

def add_bottom(matrix: list[list[chr]])-> list[list[chr]]:
    matrix.append(["."]*len(matrix[0]))
    matrix.append(["#"] * len(matrix[0]))
    return matrix

def add_sanddrop(matrix: list[list[chr]]) -> bool:
    try:
        coord = (0,matrix[0].index('+'))
    except ValueError: #plus has been overwritten so last sandrop made
        return False
    while True:
        prev_coord = coord
        coord = drop_one_step(matrix,coord[0],coord[1])
        if coord[1] < 0 or coord[1] == len(matrix[0]) or coord[0] == len(matrix)-1:
            return False

        if coord == prev_coord:
            matrix[coord[0]][coord[1]] = "o"
            return True



def drop_one_step(matrix: list[list[chr]],row,col) -> (int,int):
    if matrix[row+1][col] == ".":
        return row+1, col
    elif matrix[row + 1][col-1] == ".":
        return row + 1, col-1
    elif matrix[row + 1][col+1] == ".":
        return row + 1, col+1
    else:
        return row, col


ex14 = AdventOfCode(14)
ex14.executeTest(part1, 24)
ex14.executeTest(part2, 93)

ex14.execute(part1, part2)