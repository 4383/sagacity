from subprocess import Popen
from subprocess import PIPE


def execute(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True, check=True):
    proc = Popen(
        cmd,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
    )
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    return outs, errs
