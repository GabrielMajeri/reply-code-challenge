import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")
args = parser.parse_args()


class Developer:
    def __init__(self, company, bonus, skills):
        self.company = company
        self.bonus = bonus
        self.skills = skills

    def __repr__(self):
        return f'Developer({self.company}, {self.bonus}, {self.skills})'


class ProjectManager:
    def __init__(self, company, bonus):
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

    for _ in range(num_devs):
        info = next(fin).split()

        company = info[0]
        bonus = info[1]
        # num_skills = info[2]
        skills = set(map(encode_skill, info[3:]))

        developer = Developer(company, bonus, skills)
        devs.append(developer)

        devs_by_company[company].append(developer)

    num_pms = int(next(fin))
    print(f'PMs: {num_pms}')

    pms = []
    pms_by_company = defaultdict(list)

    for _ in range(num_pms):
        company, bonus = next(fin).split()

        bonus = int(bonus)

        pm = ProjectManager(company, bonus)
        pms.append(pm)

        pms_by_company[company].append(pm)

with open(args.output_file, 'w') as fout:
    for _ in range(num_devs):
        print('X', file=fout)
    for _ in range(num_pms):
        print('X', file=fout)
