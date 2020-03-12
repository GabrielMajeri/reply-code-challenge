import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")
args = parser.parse_args()


class Developer:
    def __init__(self, index, company, bonus, skills):
        self.index = index
        self.company = company
        self.bonus = bonus
        self.skills = skills
        self.chosen = 0

    def __repr__(self):
        return f'Developer({self.company}, {self.bonus}, {self.skills})'

    def score(self, other):
        same = len(self.skills.intersection(other.skills))
        whole = len(self.skills.union(other.skills))
        return same * (whole - same)


class ProjectManager:
    def __init__(self, index, company, bonus):
        self.index = index
        self.company = company
        self.bonus = bonus

    def __repr__(self):
        return f'PM({self.company}, {self.bonus})'


# Matrix representing the map
office = []

# List of positions where there is a developer space
dev_spaces = []
# List of positions where there is a PM space
pm_spaces = []

with open(args.input_file) as fin:
    columns, rows = map(int, next(fin).split())
    for i in range(rows):
        line = next(fin)
        for j in range(columns):
            if line[j] == '_':
                dev_spaces.append((i, j))
            elif line[j] == 'M':
                pm_spaces.append((i, j))
        office.append(line)

    print(f'Map size: {rows}x{columns}')
    print(f'Empty dev spaces: {len(dev_spaces)}')
    print(f'Empty PM spaces: {len(pm_spaces)}')

    num_devs = int(next(fin))
    print(f'Developers: {num_devs}')

    devs = []

    skill_map = dict()

    def encode_skill(skill):
        if skill not in skill_map:
            skill_map[skill] = len(skill_map)
        return skill_map[skill]

    for i in range(num_devs):
        info = next(fin).split()

        company = info[0]
        bonus = info[1]
        # num_skills = info[2]
        skills = set(map(encode_skill, info[3:]))

        developer = Developer(i, company, bonus, skills)
        devs.append(developer)

    num_pms = int(next(fin))
    print(f'PMs: {num_pms}')

    pms = []

    for i in range(num_pms):
        company, bonus = next(fin).split()

        bonus = int(bonus)

        pm = ProjectManager(i, company, bonus)
        pms.append(pm)


def matching_coef(dev1, dev2):
    sk1 = dev1.skills
    sk2 = dev2.skills
    intersect = len(sk1.intersection(sk2))
    different = len(sk1)+len(sk2) - intersect
    return abs(intersect - different)


def get_new_developer(devs):
    for dev in devs:
        if dev.chosen == 0:
            dev.chosen = 1
            return dev


def get_matching_developer(referenceDev, devs):
    mini = matching_coef(referenceDev, referenceDev)
    minidev = referenceDev.index
    for dev in devs:
        if dev.chosen == 1:
            continue
        coef = matching_coef(referenceDev, dev)
        if coef < mini:
            mini = coef
        minidev = dev

    minidev.chosen = 1
    return minidev

# print('new devs test' + str(get_new_developer(devs)))


matching_coef(devs[1], devs[2])
devPlaces = ['X'] * len(devs)

for i in range(len(office)):
    for j in range(len(office[i])):
        # if we have a developer space
        if office[i][j] == '_':
            # if we don't have any neighbours
            if ((office[i-1][j] == 'M' or office[i-1][j] == '_' or office[i-1][j] == '#')
                and (office[i][j-1] == 'M' or office[i][j-1] == '_' or office[i][j-1] == '#')
                and (office[i][j+1] == 'M' or office[i][j+1] == '_' or office[i][j+1] == '#')
                    and (office[i+1][j] == 'M' or office[i+1][j-1] == '_' or office[i+1][j-1] == '#')):
                new_dev = get_new_developer(devs)
                office[i][j] = new_dev
            elif (office[i-1][j] != 'M' and office[i-1][j] != '_' and office[i-1][j] != '#'):
                # we have neighbour on office[i-1][j]
                office[i][j] == str(get_matching_developer(
                    office[i-1][j], devs).index)
            elif (office[i+1][j] != 'M' and office[i+1][j] != '_' and office[i+1][j] != '#'):
                # we have neighbour on office[i+1][j]
                office[i][j] == str(get_matching_developer(
                    office[i+1][j], devs).index)
            elif (office[i][j-1] != 'M' and office[i][j-1] != '_' and office[i][j-1] != '#'):
                # we have neighbour on office[i][j-1]
                office[i][j] == str(get_matching_developer(
                    office[i][j-1], devs).index)
            elif (office[i][j+1] != 'M' and office[i][j+1] != '_' and office[i][j+1] != '#'):
                # we have neighbour on office[i][j+1]
                office[i][j] == str(get_matching_developer(
                    office[i][j+1], devs).index)


with open(args.output_file, 'w') as fout:
    for i in range(num_devs):
        try:
            print(str(devPlaces[i][1])+' ' +
                  str(devPlaces[i][0]), file=fout)
        except:
            print('X', file=fout)

    for i in range(num_pms):
        print('X', file=fout)
