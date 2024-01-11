import typing as TYPE
from shlex import split as shx_split
from subprocess import run as sp_run, CompletedProcess


def runcmd(
    cmd: TYPE.Union[str, TYPE.List], output: bool = True, *args, **kwargs
) -> TYPE.Optional[CompletedProcess]:
    """Runs a single command in the shell with subprocess.run
    Args:
        cmd (Union[str, List]): The command to run in the shell.
        output (bool): Whether or not to return the output of the command.
            Defaults to True.
    """
    if isinstance(cmd, str):
        cmd = shx_split(cmd)

    if output:
        return sp_run(
            cmd, check=True, text=True, capture_output=True, *args, **kwargs
        )
    else:
        sp_run(
            cmd, check=False, text=False, capture_output=False, *args, **kwargs
        )
