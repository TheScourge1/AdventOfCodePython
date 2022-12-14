from AdventOfCode import AdventOfCode


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.directories = []

    def __repr__(self):
        return self.name


def part1(data):
    directory = Directory("\\")
    read_data(data, 1, directory)
    result = all_dir_sizes(directory)
    return sum([d[1] for d in result if d[1] <= 100000])

def part2(data):
    directory = Directory("\\")
    read_data(data, 1, directory)
    result = all_dir_sizes(directory)

    result = sorted(result, key=lambda d: d[1])
    free_space = 70000000 - directory_size(directory)
    required_space = 30000000 - free_space
    for dr in result:
        if dr[1] > required_space:
            return dir[1]

    return -1


def read_data(data, location, directory):
    i = location
    while i < len(data):
        line = str(data[i]).strip()
        if line.startswith("$ ls"):
            i += 1
        elif line.startswith("$ cd"):
            if line.endswith(".."):
                return i+1
            else:
                new_directory = Directory(line.split(" ")[2])
                directory.directories.append(new_directory)
                i = read_data(data, i+1, new_directory)
        elif line.startswith("dir"):
            i += 1
        else:
            new_file = (line.split()[1], int(line.split()[0]))
            directory.files.append(new_file)
            i += 1

    return len(data)


def directory_size(directory: Directory):
    result = sum([f[1] for f in directory.files])
    for dr in directory.directories:
        result += directory_size(dr)
    return result

def all_dir_sizes(directory: Directory):
    result = [(directory.name,directory_size(directory))]
    for dr in directory.directories:
        result.extend(all_dir_sizes(dr))
    return result


ex7 = AdventOfCode(7)

ex7.executeTest(part1, 95437)
ex7.executeTest(part2, 24933642)

ex7.execute(part1, part2)