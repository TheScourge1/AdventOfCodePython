from AdventOfCode import AdventOfCode
import re


def part1(data: list[str]) -> str:
    data_grid = read_datagrid(data)
    password = read_password(data)
    location = (0, data_grid[0].index("."), 90)
    print(location)
    for s in password:
        location = walk(data_grid, location, s,False)

    return str(1000*(location[0]+1)+4*(location[1]+1)+int((location[2]+270)%360/90))


def part2(data: list[str]) -> str:
    data_grid = read_datagrid(data)
    password = read_password(data)
    location = (0, data_grid[0].index("."), 90)

    for s in password:
        location = walk(data_grid, location, s, True)

    return str(1000*(location[0]+1)+4*(location[1]+1)+int((location[2]+270)%360/90))





def walk(data_grid: list[list[str]], location: (int, int, int), command: str, is_cube:bool) -> (int, int, int):
    match command:
        case "R":
            return location[0], location[1], (location[2]+90) % 360
        case "L":
            return location[0], location[1], (location[2] + 270) % 360
        case _:
            moves = int(command)
            x, y = location[0], location[1]
            x_step = 0
            y_step = 0
            if location[2] == 0:
                x_step = -1
            elif location[2] == 90:
                y_step = 1
            elif location[2] == 180:
                x_step = 1
            elif location[2] == 270:
                y_step = -1
            else:
                raise Exception("Unknown direction: "+location[2])

            if is_cube:
                x,y = get_end_location_cube(data_grid,x,y,x_step,y_step,moves)
            else:
                x, y = get_end_location(data_grid, x, y, x_step, y_step, moves)
            return x, y, location[2]


def get_end_location(data_grid: list[list[str]], x:int, y:int, x_dir:int,y_dir:int,moves: int) -> (int,int) :
    m = 0
    result = x, y
    while m < moves:
        x1 = (x + x_dir) % len(data_grid)
        y1 = (y + y_dir) % len(data_grid[0])
        match data_grid[x1][y1]:
            case " ":
                pass
            case ".":
                result = x1, y1
                m += 1
            case "#":
                break
            case _:
                raise Exception("Unknown grid item: " + data_grid[x + x_dir][y + y_dir])
        x, y = x1, y1

    return result


def get_end_location_cube(data_grid: list[list[str]], x:int, y:int, x_dir:int,y_dir:int,moves: int) -> (int,int) :
    return x,y


def read_datagrid(data: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    max_length = max([len(line) for line in data])
    for line in data:
        new_list = list(line[:len(line)-1])
        while len(new_list) < max_length:
            new_list.append(" ")
        result.append(new_list)
    return result[:len(result)-2]


def read_password(data: list[str]) -> list[str]:
    line = data[len(data)-1]
    result = re.findall(r"(\d+|\D)", line)
    return result


ex22 = AdventOfCode(22)
ex22.executeTest(part1,"6032")
#ex22.executeTest(part2,"5031")

ex22.execute(part1,part2)