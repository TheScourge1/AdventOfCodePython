from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    line = data[0].strip()
    front_counter = 0
    front_remaining = int(line[front_counter])
    back_counter = len(line)-1
    back_remaining = int(line[back_counter])
    target_position = 0
    result = 0
    res_str = ""
    while front_counter < back_counter:
        while front_remaining > 0:
            result += (front_counter // 2) * target_position
            res_str += str(front_counter // 2) + " "
            target_position += 1
            front_remaining -= 1
        gap_remaining = int(line[front_counter+1])
        while gap_remaining > 0:
            while back_remaining == 0:
                back_counter -= 2
                back_remaining = int(line[back_counter])
            if back_counter <= front_counter:
               break

            result += (back_counter // 2) * target_position
            res_str += str(back_counter // 2) + " "
            target_position += 1
            gap_remaining -= 1
            back_remaining -= 1

        front_counter += 2
        front_remaining = int(line[front_counter])

    while back_remaining > 0 and front_counter == back_counter:
        result += (back_counter // 2) * target_position
        res_str += str(back_counter // 2) + " "
        back_remaining -= 1
        target_position += 1

    return result


def part2(data: list[str]):
    pass


ex = AdventOfCode(9)
ex.executeTest(part1, 1928)

ex.execute(part1,part2)