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


columns, rows = map(int, input().split())

# Matrix representing the map
office = []

# List of positions where there is a developer space
dev_spaces = []
# List of positions where there is a PM space
pm_spaces = []

for i in range(rows):
    line = input()
    for j in range(columns):
        if line[j] == '_':
            dev_spaces.append((i, j))
        elif line[j] == 'M':
            pm_spaces.append((i, j))
    office.append(line)

print(f'Map size: {rows}x{columns}')
print(f'Empty dev spaces: {len(dev_spaces)}')
print(f'Empty PM spaces: {len(pm_spaces)}')

num_devs = int(input())
print(f'Developers: {num_devs}')

devs = []

skill_map = dict()


def encode_skill(skill):
    if skill not in skill_map:
        skill_map[skill] = len(skill_map)
    return skill_map[skill]


for _ in range(num_devs):
    info = input().split()

    company = info[0]
    bonus = info[1]
    # num_skills = info[2]
    skills = set(map(encode_skill, info[3:]))

    developer = Developer(company, bonus, skills)
    devs.append(developer)

num_pms = int(input())
print(f'PMs: {num_pms}')

pms = []

for _ in range(num_pms):
    company, bonus = input().split()

    bonus = int(bonus)

    pm = ProjectManager(company, bonus)
    pms.append(pm)
