from AdventOfCode import AdventOfCode
from icecream import ic

def part1(data: list[str]) -> str:
    total_amount = sum([convert_to_decimal(line.strip()) for line in data])
    print(f"total amount: {total_amount}")

    if total_amount != convert_to_decimal(convert_to_snafu(total_amount)):
        raise Exception(f"Expected:{total_amount} converted: {convert_to_decimal(convert_to_snafu(total_amount))}")

    return convert_to_snafu(total_amount)


def part2(data: list[str]) -> str:
    pass


def convert_to_decimal(decimal: str) -> int:
    result = 0
    for i in range(0, len(decimal)):
        digit = convert_digit(decimal[len(decimal)-1 -i :len(decimal)-i])
        result += digit * (5**i)

    return result


def convert_to_snafu(number: int) -> str:
    temp_value = number
    result = ""
    factor = 0

    while temp_value > 5 ** factor:
        factor += 1

    while factor >= 0:
        base_val = 5 ** factor
        lower_boundary = 2 * sum([5 ** i for i in range(factor-1, -1, -1)])
        if temp_value >= 3 * base_val:
            raise Exception(f"to high current value found: {temp_value} for base: {base_val}")
        elif 2 * base_val + lower_boundary >= temp_value >= 2 * base_val - lower_boundary:
            temp_value -= 2 * base_val
            result += "2"
        elif base_val + lower_boundary >= temp_value >= base_val - lower_boundary:
            temp_value -= base_val
            result += "1"
        elif lower_boundary >= temp_value >= - lower_boundary:
                result += "0"
        elif - base_val + lower_boundary >= temp_value >= - base_val - lower_boundary:
            temp_value += base_val
            result += "-"
        elif - 2 * base_val + lower_boundary >= temp_value >= - 2 * base_val - lower_boundary:
            temp_value += 2 * base_val
            result += "="
        else:
            raise Exception(f"to low current value found: {temp_value} for base: {base_val}")

        factor -= 1

    return result[1:] if len(result) > 1 and result[0] == "0" else result


def convert_digit(digit: str) -> int:
    match digit:
        case "O":
            return 0
        case "1":
            return 1
        case "2":
            return 2
        case "-":
            return -1
        case "=":
            return -2
        case _:
            Exception("Unexpected character: "+digit)
    return 0


ex25 = AdventOfCode(25)
ex25.executeTest(part1, "2=-1=0")

ex25.execute(part1, part2)