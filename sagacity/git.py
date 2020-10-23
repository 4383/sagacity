import sys

from sagacity import execute


SEP = "ø"


def fetch(remote='--all'):
    cmd = ['git', 'fetch', remote]
    outs, errs = execute.execute(cmd)
    if errs:
        print(errs)
        sys.exit(200)


def log(since=None, until=None,
        pretty=f'%cd{SEP}%an{SEP}%ae{SEP}%H', no_merges=True, fetching=True,
        remote_to_fetch='origin', branch=None,
        path=None):
    if fetching:
        fetch(remote_to_fetch)
    cmd = ['git', 'log']
    if since:
        cmd.extend(['--since', since.strftime("%b %d %Y")])
    if until:
        cmd.extend(['--until', until.strftime("%b %d %Y")])
    if pretty:
        cmd.append(f'--pretty=format:{pretty}')
    if no_merges:
        cmd.append('--no-merges')
    if branch:
        cmd.append(branch)
    if path:
        cmd.extend(['--', path])
    outs, errs = execute.execute(cmd, shell=False)
    if errs:
        print(errs)
        sys.exit(201)
    return outs.decode('utf-8'), errs.decode('utf-8')
