from AdventOfCode import AdventOfCode


def part1(data):
    rope = [(0, 0)]*2
    tail_visits = {(0, 0)}
    for line in data:
        command = line.split(" ")
        action = command[0]
        for i in range(0, int(command[1])):
            rope = move_rope(rope, action)
            tail_visits.add(rope[len(rope)-1])

    return len(tail_visits)


def part2(data):
    rope = [(0, 0)]*10
    tail_visits = {(0, 0)}
    for line in data:
        command = line.split(" ")
        action = command[0]
        for i in range(0, int(command[1])):
            rope = move_rope(rope, action)
            check_rope(rope)
            tail_visits.add(rope[len(rope)-1])

    return len(tail_visits)


def move_rope(rope, command):
    commands = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
    action = commands.get(command)
    new_rope = [(rope[0][0]+action[0], rope[0][1]+action[1])]
    for i in range(1, len(rope)):
        new_rope.append(move_tail(new_rope[i-1], rope[i]))

    return new_rope


def move_tail(head_location, tail_location):
    h_dist = head_location[0]-tail_location[0]
    v_dist = head_location[1]-tail_location[1]

    if abs(h_dist) == 2:
        if abs(v_dist) == 2:
            return tail_location[0] + correct_move(h_dist), tail_location[1] + correct_move(v_dist)
        else:
            return tail_location[0] + correct_move(h_dist), tail_location[1] + v_dist
    elif abs(v_dist) == 2:
        return tail_location[0] + h_dist, tail_location[1] + correct_move(v_dist)
    else:
        return tail_location


def correct_move(dist):
    return int(dist/abs(dist)) if abs(dist) == 2 else 0


def check_rope(rope):
    for i in range(0, len(rope)-1):
        if abs(rope[i][0]-rope[i+1][0])>2 or abs(rope[i][1]-rope[i+1][1])>2:
            raise Exception(f"invalid rope: {rope}")


def print_matrix(visits):
    rows = []
    matrix_top = max([visit[0] for visit in visits]+[visit[1] for visit in visits])+1
    matrix_bottom = min([visit[0] for visit in visits] + [visit[1] for visit in visits])
    for j in range(matrix_bottom,matrix_top):
        row = ""
        for i in range(matrix_bottom,matrix_top):
            if (i,j) in visits:
                row += "# "
            else:
                row += ". "
        rows.append(row)

    rows.reverse()
    for row in rows:
        print(row)


ex09 = AdventOfCode(9)

ex09.executeTest(part1, 13)
ex09.executeTest(part2, 1)
ex09.executeTest(part2, 36, 2)

ex09.execute(part1, part2)
