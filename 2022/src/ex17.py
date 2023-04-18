from AdventOfCode import AdventOfCode
from dataclasses import dataclass

@dataclass
class Canvas:
    view: list[list[int]]
    last_block_dropped: list[int]
    height: int = 0
    _canvas_size = 100000

    def __init__(self):
        self.view = []
        self.last_block_dropped = [0] * self._canvas_size
        self.view.append([1] * 7)
        for i in range(0,self._canvas_size):
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
        index = drop_bloc(canvas, blocs[i % 5], index, data[0],i)

    #print_range(canvas.view[0:3200])
    return str(canvas.height)


def part2(data: list[str]):
    canvas = Canvas()
    index = 0

    for i in range(0, 50000):
        index = drop_bloc(canvas, blocs[i % 5], index, data[0],i+1)

    string_canvas = "".join([str(conv_bits(row))+ "" for row in canvas.view])

    for i in range(0, int(index/2)):
        next_occurance = string_canvas[i+10:].find(string_canvas[i:i+10])+i+10
        if next_occurance > 0 and string_canvas[i:next_occurance] == string_canvas[next_occurance:next_occurance+next_occurance-i]:
            blocs_before_rep = canvas.last_block_dropped[i]
            start_rep = i
            rep_height = next_occurance - start_rep
            blocs_in_rep = canvas.last_block_dropped[next_occurance] - blocs_before_rep
            number_of_reps = int((1000000000000 - blocs_before_rep) / blocs_in_rep)
            remaining_blocks = 1000000000000 - blocs_before_rep - blocs_in_rep * number_of_reps

            remaining_height = 0
            start_block = canvas.last_block_dropped[i]
            for itt in range(i,next_occurance+1):
                if canvas.last_block_dropped[itt]-start_block == remaining_blocks:
                    remaining_height = itt-i

            total_height = start_rep + rep_height*number_of_reps + remaining_height
            return str(total_height)

    return -1


def conv_bits(input: list[int]) -> str:
    res = input[0]
    for i in input[1:]:
        res = res*2+i
    return chr(65+res)

def drop_bloc(canvas: Canvas, next_bloc: list[list[int]], index: int, moves: str, block_index) -> int:
    h_offset = 2
    v_offset = canvas.height + 4

    while True:
        next_move = moves[index % len(moves)]
        index += 1
        new_h_offset = horizontal_move(next_move, next_bloc, h_offset)
        if not block_overlapping(canvas, new_h_offset, v_offset, next_bloc):
            h_offset = new_h_offset
        if block_overlapping(canvas, h_offset, v_offset-1, next_bloc):
            break
        v_offset -= 1

    write_bloc(canvas, h_offset, v_offset, next_bloc, block_index)

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

def write_bloc(canvas: Canvas, h_offset: int, v_offset: int, bloc: list[list[int]],block_index: int):
    for i in range(0,len(bloc)):
        canvas.last_block_dropped[i+v_offset] = block_index
        for j in range(0, len(bloc[0])):
            if bloc[i][j] == 1:
                canvas.view[v_offset+i][j+h_offset] = 1

    canvas.height = max(v_offset + len(bloc)-1, canvas.height)


def print_range(grid: list[list[int]]):
    print_grid = grid.copy()
    print_grid.reverse()
    for line in print_grid:
        str = ''.join([('.' if l == 0 else '#') for l in line])
        print(str)
    print()


ex17 = AdventOfCode(17)
ex17.executeTest(part1, "3068")
ex17.executeTest(part2, "1514285714288")

ex17.execute(part1, part2)