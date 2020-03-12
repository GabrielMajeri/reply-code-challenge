import argparse
from collections import defaultdict
import random
from tqdm import tqdm


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
    devs_by_company = defaultdict(list)

    skill_map = dict()

    def encode_skill(skill):
        if skill not in skill_map:
            skill_map[skill] = len(skill_map)
        return skill_map[skill]

    for index in range(num_devs):
        info = next(fin).split()

        company = info[0]
        bonus = int(info[1])
        # num_skills = info[2]
        skills = set(map(encode_skill, info[3:]))

        developer = Developer(index, company, bonus, skills)
        devs.append(developer)

        devs_by_company[company].append(developer)

    num_pms = int(next(fin))
    print(f'PMs: {num_pms}')

    pms = []
    pms_by_company = defaultdict(list)

    for index in range(num_pms):
        company, bonus = next(fin).split()

        bonus = int(bonus)

        pm = ProjectManager(index, company, bonus)
        pms.append(pm)

        pms_by_company[company].append(pm)


def run_with_seed(seed):
    random.seed(seed)

    places = dict()

    dev_positions = dict()
    random.shuffle(devs)
    for space, dev in zip(dev_spaces, devs):
        dev_positions[dev.index] = space
        places[space] = dev

    pm_positions = dict()
    random.shuffle(pms)
    for space, pm in zip(pm_spaces, pms):
        pm_positions[pm.index] = space
        places[space] = pm

    return places, dev_positions, pm_positions


max_score = 0
max_seed = 0

for seed in tqdm(range(50000)):
    places, _, _ = run_with_seed(seed)

    def score_pair(a, b):
        if isinstance(a, ProjectManager):
            return a.bonus * b.bonus if a.company == b.company else 0
        else:
            if isinstance(b, ProjectManager):
                return a.bonus * b.bonus if a.company == b.company else 0
            else:
                return a.score(b)

    def score_position(row, col):
        position = (row, col)
        if position not in places:
            return 0

        employee = places[(row, col)]

        score = 0
        if (row, col + 1) in places:
            other = places[(row, col + 1)]
            score += score_pair(employee, other)

        if (row + 1, col) in places:
            other = places[(row + 1, col)]
            score += score_pair(employee, other)

        return score

    total_score = 0
    for row, col in places.keys():
        total_score += score_position(row, col)

    if total_score > max_score:
        max_score = total_score
        max_seed = seed

print('Max score:', max_score, 'for seed', max_seed)

_, dev_positions, pm_positions = run_with_seed(max_seed)

with open(args.output_file, 'w') as fout:
    for idx in range(len(devs)):
        if idx in dev_positions:
            position = dev_positions[idx]
            print(position[1], position[0], file=fout)
        else:
            print('X', file=fout)

    for idx in range(len(pms)):
        if idx in pm_positions:
            position = pm_positions[idx]
            print(position[1], position[0], file=fout)
        else:
            print('X', file=fout)
