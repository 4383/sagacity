#!/usr/bin/python
import argparse
import datetime
import os
import sys

import pkg_resources

from sagacity import git
from sagacity import render
from sagacity.git import SEP


def project_path(string):
    if os.path.isdir(string):
        return string
    raise argparse.ArgumentTypeError(
        f'Given project path is not a dir ({string})')


def path_file(string):
    if os.path.isdir(string) or os.path.isfile(string):
        return string
    raise argparse.ArgumentTypeError(
        f'Should be a valid path or a file ({string})')


# arguments parsing
def argparser():
    epilog = 'Visit https://github.com/4383/sagacity'

    parser = argparse.ArgumentParser(
        description='Visualize deep patterns in your projects histories.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog)
    parser.add_argument(
        'project',
        nargs='?',
        type=project_path, default='.',
        help="Path to audit. Default set to the current dir"
    )
    parser.add_argument(
        '--since',
        default='1940-03-10',
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help="Date the analysis begins")
    parser.add_argument(
        '--until',
        default=datetime.datetime.now().strftime('%Y-%m-%d'),
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help="Date the analysis ends")
    parser.add_argument(
        '--path',
        default=None,
        help='Observe the activity of a specific path or file')
    parser.add_argument(
        '--branch',
        default=None,
        help='Observe the activity of a specific branch')
    parser.add_argument(
        '--render',
        default='chartjs',
        help='Display data by using a specific render. Default set to chartjs'
    )
    parser.add_argument(
        '-o', '--output',
        type=argparse.FileType('w'),
        help='Write output into the specified file'
    )
    parser.add_argument('-s', '--silent', action='store_true',
                        help="silent mode, doesn't display message when \
                        element was not found")
    parser.add_argument('-v', '--version', action='store_true',
                        help="print the sagacity version number and \
                        exit (also --version)")
    parser.add_argument('--debug', action='store_true',
                        help="Activate the debug mode (based on pdb)")
    return parser.parse_args()


def to_json(data):
    json_data = []
    for line in data.split("\n"):
        date, author, email, sha = line.split(SEP)
        json_data.append({
            'x': "newDateString('{out_date}')".format(
                out_date=datetime.datetime.strptime(
                date, "%a %b %d %H:%M:%S %Y %z").strftime('%d/%m/%Y %H:%M')),
            'y': 1,
            #'author': author,
            #'email': email,
            #'sha': sha
        })
    return json_data


def get_data(since=None, until=None, path=None, branch=None):
    outs, errs = git.log(since=since, until=until, path=path, branch=branch)
    return to_json(outs)


def version():
    installed = pkg_resources.get_distribution('sagacity').version
    print("sagacity version {}".format(installed))


# Main
def main():
    if '-v' in sys.argv or '--version' in sys.argv:
        version()
        sys.exit(0)
    args = argparser()
    if args.debug:
        import pdb
        pdb.set_trace()
    pcwd = os.getcwd()
    if args.project != '.':
        os.chdir(args.project)
    dataset = get_data(
        since=args.since,
        until=args.until,
        path=args.path,
        branch=args.branch
    )
    silent = args.silent
    if not hasattr(render, args.render):
        print(f"Renderer not found ({args.render})")
        sys.exit(1)
    labels = []
    since = datetime.date(args.since.year, args.since.month, args.since.day)
    until = datetime.date(args.until.year, args.until.month, args.until.day)
    delta =  until - since
    render_func = getattr(render, args.render)
    for i in range(delta.days + 1):
        dated = since + datetime.timedelta(days=i)
        labels.append(dated.strftime('"%d/%m/%Y"'))
    output = render_func(labels, dataset)
    if args.output:
        args.output.write(output)
    else:
        print(output)
    cwd = os.getcwd()
    if pcwd != cwd:
        os.chdir(pcwd)
