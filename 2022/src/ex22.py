from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import re


@dataclass
class Location:
    x: int = 0
    y: int = 0
    direction: int = 0
    face_id = 1

    def __init__(self, x, y, direction, face_id = 1):
        self.x = x
        self.y = y
        self.direction = direction
        self.face_id = face_id

    def __repr__(self):
        return f"({self.x},{self.y},{self.direction},f{self.face_id})"

    def get_move_vector(self) -> (x,y):
        match self.direction:
            case 0:
                return -1, 0
            case 90:
                return 0, 1
            case 180:
                return 1, 0
            case 270:
                return 0, -1
            case _:
                raise Exception("Unknown direction: " + str(self.direction))


    def turn_R(self):
        return Location(self.x,self.y,(self.direction+90) % 360, self.face_id)

    def turn_L(self):
        return Location(self.x,self.y,(self.direction+270) % 360, self.face_id)

    def get_value(self):
        return 1000 * (self.x + 1) + 4 * (self.y + 1) + int((self.direction + 270) % 360 / 90)


def part1(data: list[str]) -> str:
    data_grid = read_datagrid(data)
    password = read_password(data)
    location = Location(0, data_grid[0].index("."), 90)
    for s in password:
        location = walk(data_grid, location, s, False)

    return str(location.get_value())


def part2(data: list[str]) -> str:
    data_grid = read_datagrid(data)
    password = read_password(data)
    location = Location(0, 0, 90)

    print(location)
    for s in password:
        location = walk(data_grid, location, s, True)
        print(location)

    cube_location = cube_to_grid_location(data_grid,location)

    return str(cube_location.get_value())


def walk(data_grid: list[list[str]], location: Location, command: str, is_cube:bool) -> Location:
    match command:
        case "R":
            return location.turn_R()
        case "L":
            return location.turn_L()
        case _:
            moves = int(command)
            if is_cube:
                return move_forward_cube(data_grid,location,moves)
            else:
                return move_forward(data_grid, location, moves)


def move_forward(data_grid: list[list[str]], location: Location, moves: int) -> Location:
    m = 0
    x = location.x
    y = location.y
    x_dir, y_dir = location.get_move_vector()
    result = location
    while m < moves:
        x1 = (x + x_dir) % len(data_grid)
        y1 = (y + y_dir) % len(data_grid[0])
        match data_grid[x1][y1]:
            case " ":
                pass
            case ".":
                result = Location(x1, y1,location.direction)
                m += 1
            case "#":
                break
            case _:
                raise Exception("Unknown grid item: " + data_grid[x + x_dir][y + y_dir])
        x, y = x1, y1

    return result


def move_forward_cube(data_grid: list[list[str]],location:Location, moves: int) -> Location :
    cube_size = int(len(data_grid) /3)

    """""  face_id = location.face_id
    for face_id in range(1,7):
        print(f"face: {face_id}")
        for x in range(0,cube_size):
            line = ""
            for y in range(0,cube_size):
                line += get_face_item(data_grid,Location(x,y,0))
            print(line)

        print("")
    """""
    m = 0
    current_location = location
    result = current_location
    while m < moves:
        potential_new_location = get_next_cube_location(cube_size,current_location)
        match get_face_item(data_grid,potential_new_location):
            case " ":
                raise Exception("Unexpected white space found")
            case ".":
                result = potential_new_location
                m += 1
            case "#":
                break
            case _:
                raise Exception("Unknown grid item: " + get_face_item(data_grid,potential_new_location))
        current_location = potential_new_location

    return result


def get_face_item(data_grid: list[list[str]], location: Location) -> str:
    grid_location = cube_to_grid_location(data_grid,location)
    return data_grid[grid_location.x][grid_location.y]


def cube_to_grid_location(data_grid, location:Location) -> Location:
    cube_size = int(len(data_grid) / 3)
    offsets = {1: (0, 2), 2: (1, 0), 3: (1, 1), 4: (1, 2), 5: (2, 2), 6: (2, 3)}
    face_id = location.face_id
    x = cube_size*offsets[face_id][0]+location.x
    y = cube_size*offsets[face_id][1]+location.y

    return Location(x, y, location.direction, 1)


def get_next_cube_location(cube_size:int, location:Location) -> Location:
    adjacent_grids = {(1, 0):  {1:(4,0), 2:(1,180), 3:(5,270), 4:(5,0), 5:(2,180), 6:(5,180)},
                      (-1, 0): {1:(2,180), 2:(5,180), 3:(1,90), 4:(1,0), 5:(4,0), 6:(5,180)},
                      (0, 1):  {1:(6,180), 2:(3,0), 3:(4,0), 4:(6,90), 5:(2,180), 6:(2,270)},
                      (0, -1): {1:(3,270), 2:(5,180), 3:(2,0), 4:(3,0), 5:3, 6:(1,180)}}

    x_dir, y_dir = location.get_move_vector()
    x, y = location.x, location.y
    face_id = location.face_id

    if x + x_dir < 0:
        new_face_id = adjacent_grids[(-1,0)][face_id][0]
        rotation = adjacent_grids[(-1,0)][face_id][1]
    elif x + x_dir >= cube_size:
        new_face_id = adjacent_grids[(1, 0)][face_id][0]
        rotation = adjacent_grids[(1, 0)][face_id][1]
    elif y + y_dir < 0:
        new_face_id = adjacent_grids[(0,-1)][face_id][0]
        rotation = adjacent_grids[(0, -1)][face_id][1]
    elif y + y_dir >= cube_size:
        new_face_id = adjacent_grids[(0, 1)][face_id][0]
        rotation = adjacent_grids[(0, 1)][face_id][1]
    else:
        rotation = 0
        new_face_id = location.face_id

    new_direction = (location.direction + rotation) % 360
    match rotation:
        case 0:
            new_x, new_y = (x + x_dir + cube_size) % cube_size, (y + y_dir + cube_size) % cube_size
        case 180:
            new_x, new_y = x, y
        case 90:
            new_x, new_y = (y + y_dir + cube_size) % cube_size, (x + x_dir + cube_size) % cube_size
        case 270:
            new_x, new_y = y, x

    return Location(new_x, new_y, new_direction, new_face_id)


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
ex22.executeTest(part2,"5031")

ex22.execute(part1,part2)