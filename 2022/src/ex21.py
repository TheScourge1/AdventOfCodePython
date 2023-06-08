from AdventOfCode import AdventOfCode
from dataclasses import dataclass



def part1(data:list[str]) -> str:
    commands = read_data(data)
    return str(get_value("root",commands))


def part2(data:list[str]) -> str:
    commands = read_data(data)
    root_command = commands["root"]
    if contains_human(root_command[0],commands):
        return str(get_equality_value(root_command[0],get_value(root_command[2],commands),commands))
    else:
        return str(get_equality_value(root_command[2], get_value(root_command[0],commands),commands))


def get_equality_value(name: str, value: int, commands: dict[str, list[str]]) -> int:
    command = commands[name]
    if contains_human(command[2],commands):
        left_value = get_value(command[0],commands)
        match command[1]:
            case "+":
                equal_value = value - left_value
            case "-":
                equal_value = - (value - left_value)
            case "*":
                equal_value = int(value/left_value)
            case "/":
                equal_value = int(left_value / value)
            case "_":
                raise Exception("Unknown command" + command[1])
        if command[2] == "humn":
            return equal_value
        else:
            return get_equality_value(command[2],equal_value,commands)
    elif contains_human(command[0], commands):
        right_value = get_value(command[2],commands)
        match command[1]:
            case "+":
                equal_value = value - right_value
            case "-":
                equal_value = value + right_value
            case "*":
                equal_value = int(value/right_value)
            case "/":
                equal_value = value * right_value
            case "_":
                raise Exception("Unknown command" + command[1])
        if command[0] == "humn":
            return equal_value
        else:
            return get_equality_value(command[0], equal_value, commands)

    else:
        raise Exception("humn command not found at: " + name)

def get_value(name: str, commands: dict[str, list[str]]) -> int:
    command = commands[name]
    if len(command) == 1:
        return int(command[0])
    else:
        left = get_value(command[0],commands)
        right = get_value(command[2],commands)
        match command[1]:
            case "+":
                result = left + right
            case "-":
                result = left - right
            case "*":
                result = left * right
            case "/":
                result = int(left / right)
            case "_":
                raise Exception("Unknown command"+command[1])
        return result


def contains_human(name: str, commands: dict[str, list[str]]) -> bool:
    command = commands[name]
    if len(command) == 1:
        return name == "humn"
    elif command[0] == "humn" or command[2] == "humn":
        return True
    else:
        return contains_human(command[0],commands) or contains_human(command[2],commands)

def read_data(data:list[str]) -> dict[str, list[str]]:
    result = {}
    for line in data:
        line_split = line.strip().split(" ")
        name = line_split[0][0:4]
        if len(line_split) == 2:
            result[name] = [line_split[1]]
        else:
            result[name] = [line_split[1], line_split[2], line_split[3]]
    return result

ex21 = AdventOfCode(21)
ex21.executeTest(part1,"152")
ex21.executeTest(part2,"301")

ex21.execute(part1,part2)