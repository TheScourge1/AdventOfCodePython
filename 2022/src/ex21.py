from AdventOfCode import AdventOfCode
from dataclasses import dataclass



def part1(data:list[str]) -> str:
    commands = read_data(data)
    for c in commands:
        print(c + str(commands[c]))

    return str(get_value("root",commands))


def part2(data:list[str]) -> str:
    pass


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
ex21.executeTest(part1,"301")

ex21.execute(part1,part2)