from AdventOfCode import AdventOfCode
from dataclasses import dataclass

@dataclass
class Canvas:
    view: list[list[int]]
    height: int = 0

    def __init__(self):
        self.view = []
        self.view.append([1] * 7)
        for i in range(0,50000):
            self.view.append([0]*7)

blocs = [[[1,1,1,1]],
        [[0,1,0],[1,1,1],[0,1,0]],
        [[1,1,1],[0,0,1],[0,0,1]],
        [[1],[1],[1],[1]],
        [[1,1],[1,1]]]


def part1(data: list[str]):
    canvas = Canvas()
    index = 0
    for i in range(0, 2022):
        index = drop_bloc(canvas,blocs[i % 5], index, data[0])
        #print_range(canvas.view[0:10])

    print_range(canvas.view[0:3200])
    return str(canvas.height)


def drop_bloc(canvas: Canvas, next_bloc: list[list[int]], index: int, moves: str) -> int:
    h_offset = 2
    v_offset = canvas.height + 4

    while True:
        next_move = moves[index % len(moves)]
        index+=1
        new_h_offset = horizontal_move(next_move, next_bloc, h_offset)
        if not block_overlapping(canvas, new_h_offset, v_offset, next_bloc):
            h_offset = new_h_offset
           # print("move 1: "+next_move+" "+str(h_offset))
        else:
            pass
           # print("skip h_move: "+ str(new_h_offset))
        if block_overlapping(canvas, h_offset, v_offset-1, next_bloc):
            break
        v_offset -= 1
        #print("drop 1: " + str(v_offset))

    for i in range(0,len(next_bloc)):
        for j in range(0,len(next_bloc[0])):
            canvas.view[v_offset+i][j+h_offset] = next_bloc[i][j]

    canvas.height = max(v_offset + len(next_bloc)-1,canvas.height)
    #print("canvast height: "+str(canvas.height))
    return index


def horizontal_move(next_move: str, bloc: list[list[int]], h_offset: int) -> int:
    if next_move == '>':
        if h_offset + len(bloc[0]) < 7:
            return h_offset + 1
        else:
            return h_offset
    elif next_move == '<':
        if h_offset > 0:
            return h_offset - 1
        else:
            return h_offset
    else:
        raise Exception("Unexpected move found: " + next_move + "_")


def block_overlapping(canvas: Canvas, h_offset: int, v_offset: int, bloc: list[list[int]]) -> bool:
    for i in range(0, len(bloc)):
        for j in range(0, len(bloc[0])):
            if canvas.view[v_offset+i][j+h_offset] == 1 and bloc[i][j] == 1:
                return True
    return False

def part2(data: list[str]):
    pass


def print_range(grid: list[list[int]]):
    print_grid = grid.copy()
    print_grid.reverse()
    for line in print_grid:
        str = ''.join([('.' if l == 0 else '#') for l in line])
        print(str)
    print()


ex17 = AdventOfCode(17)
ex17.executeTest(part1,"3068")

ex17.execute(part1, part2) #3133 to low