#!/usr/bin/env python3
import sys
from pyshared import Dict, List, U

struct = [
    {
        'c1': [
            'a1',
            {
                'sc1': [
                    'a2',
                    {'sc2': ['a3', 'a4', {'sc3': ['a5', {'sc4': ['a6']}]}]},
                ]
            },
        ]
    },
    {
        'c2': [
            {
                'sc5': [
                    {
                        'sc6': [
                            {
                                'sc7': [
                                    {
                                        'sc8': [
                                            {
                                                'sc9': [
                                                    {'sc10': ['a7']},
                                                    {'sc11': ['a8']},
                                                ]
                                            },
                                            {'sc12': ['a9']},
                                        ]
                                    },
                                    {'sc13': ['a10']},
                                ]
                            },
                            {'sc14': ['a11']},
                        ]
                    },
                    {'sc15': ['a12']},
                ]
            },
            {'sc16': ['a13']},
            'a14',
        ]
    },
    {'command': ['arg']},
    {'diffcmd': []},
]


def get_aliases(name: str, group: List[str]) -> List[str]:
    name_chars = list(name)
    shortest = ''
    group = [x for x in group if x != name]
    while name_chars:
        shortest = f'{shortest}{name_chars.pop(0)}'
        if not any([shortest in arg for arg in group]):
            break
    return [shortest, f'-{shortest}', f'--{shortest}']


class Cmd:
    group = List[str]

    def __init__(self, obj: Dict, group: List[U[Dict, str]] = []):
        self.obj = obj
        self.name = list(obj.keys())[0]
        _vals = obj[self.name]
        self.args = [s for s in _vals if isinstance(s, str)]
        self.subcmds = [s for s in _vals if isinstance(s, dict)]
        self.group = group

    def __repr__str__(self):
        return (
            f'<Cmd: {self.name} ({self.short}) <ARGS {self.args}>'
            f' <SUBCMDS {self.subcmds}>>'
        )

    def __str__(self):
        return self.__repr__str__()

    def __repr__(self):
        return self.__repr__str__()

    @property
    def short(self):
        return get_aliases(self.name, self.group)[0]

    @property
    def aliases(self):
        return get_aliases(self.name, self.group)


class Arg:
    def __init__(self, obj: str, group):
        self.obj = obj
        self.name = obj
        self.group = group

    def __repr__str__(self):
        return f'<Arg: {self.name} ({self.short})>'

    def __str__(self):
        return self.__repr__str__()

    def __repr__(self):
        return self.__repr__str__()

    @property
    def short(self):
        return get_aliases(self.name, self.group)[0]


def cmd_or_arg(obj, group):
    if isinstance(obj, dict):
        return Cmd(obj, group)
    return Arg(obj, group)


def parse(struct: List[U[str, Dict]]) -> List[U[Cmd, Arg]]:
    all_keys = [list(x.keys())[0] for x in struct if isinstance(x, dict)]
    group = all_keys + [x for x in struct if isinstance(x, str)]

    cmds = [Cmd(c, group) for c in struct if isinstance(c, dict)]

    return cmds


real_struct = [
    {'list': ['--secret']},
    {'add': ('--secret', '--name')},
    {
        'remote': [
            {'push': []},
            {'pull': []},
            {'init': []},
            {'delete': []},
            {'list': ['secret']},
        ]
    },
    {'info': []},
]

parsed = parse(real_struct)
print(parsed)

print(parse(struct))
