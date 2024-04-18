class Arg:
    def __init__(self, name, group):
        self.name = name
        self.aliases = get_aliases(name, group)

    def __str__(self):
        return f"<Arg: {self.name} Aliases: {self.aliases}>"


class Cmd:
    def __init__(self, name, args, group):
        self.name = name
        subgroup = [name]
        subgroup.extend(
            k
            for x in [z for z in args if isinstance(z, dict)]
            for k in x.keys()
            if isinstance(x, dict)
        )
        self.aliases = get_aliases(name, group)
        self.subcmds = []
        for x in args:
            if isinstance(x, dict):
                for k, v in x.items():
                    self.subcmds.append(Cmd(k, v, subgroup))
            else:
                self.subcmds.append(Arg(x, subgroup))

    def __str__(self):
        subcmds_str = ', '.join(str(subcmd) for subcmd in self.subcmds)
        return f"<Cmd: {self.name} Aliases: {self.aliases} Subcmds: [{subcmds_str}]>"


def get_aliases(name, group):
    for length in range(1, len(name) + 1):
        alias = name[:length]
        if not any(
            other.startswith(alias) for other in group if other != name
        ):
            return [alias, f'-{alias}', f'--{alias}']
    return [name, f'-{name}', f'--{name}']


def parse_short(commands):
    parsed_cmds = []
    for cmd in commands:
        for name, args in cmd.items():
            group = [name]
            group.extend(
                k
                for x in [z for z in args if isinstance(z, dict)]
                for k in x.keys()
                if isinstance(x, dict)
            )
            parsed_cmds.append(Cmd(name, args, group))
    return parsed_cmds


commands = [
    {'list': ['secret']},
    {'add': [{'secret': []}, {'name': []}]},
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
