#!/usr/bin/env python

# Copyright 2015 Massachusetts Institute of Tech

"""
A convenience tool for creating metaprojects.

Usage:
  >> metaproject init my_project
  >> metaproject add <git url> <dependencies>
"""

import os
import shutil
import argparse
from git import Repo

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def initialize(args):
    """Initialize a metaproject."""

    join = os.path.join

    print GREEN + "Metaproject destination:"
    print BLUE + "  %s" % args.path
    root_dir = os.path.dirname(os.path.realpath(__file__))
    src = join(root_dir, "template/")
    shutil.copytree(src, args.path)

    # Rename metaproject in README.md.
    src_split = os.path.split(args.path)
    name = src_split[-1]
    contents = ""
    with open(join(args.path, "README.md"), "r") as readme:
        contents = readme.read()

    contents = contents.replace('metaproject', name)

    with open(join(args.path, "README.md"), "w") as readme:
        readme.write(contents)

    # Add a gitignore.
    with open(join(args.path, ".gitignore"), "w") as gitignore:
        ignores = []
        ignores.append("build\n")
        ignores.append("install\n")
        ignores.append("*~\n")
        ignores.append("*pyc\n")

        gitignore.writelines(ignores)

    # Initialize repo.
    print GREEN + "Initializing repository:"
    print BLUE + "  git init %s" % args.path
    print BLUE + "  cd %s" % args.path
    print BLUE + "  git add ."
    print BLUE + "  git commit -m \"Initialize metaproject.\""

    repo = Repo.init(args.path)
    repo.git.add(all=True)
    repo.index.commit("Initialize metaproject.")

    return

def add_submodule(args):
    """Add a git submodule to the metaproject."""
    print args.url
    print args.dependencies
    return

def main():
    """Main entry point for metaproject."""

    # Parse args.
    parser = argparse.ArgumentParser(description="A convenience tool for creating metaprojects.")
    subparsers = parser.add_subparsers(help='Sub-command help')

    # Parser for init command.
    init_parser = subparsers.add_parser('init', help='Initialize a metaproject')
    init_parser.add_argument('path', help='Path to metaproject.')
    init_parser.set_defaults(func=initialize)

    # Parser for add command.
    add_parser = subparsers.add_parser('add', help='Add a project to the metaproject as a git ' +
                                       'submodule.')
    add_parser.add_argument('url', help='Git repository url')
    add_parser.add_argument('dependencies', nargs='+', help='Project dependencies.')
    add_parser.set_defaults(func=add_submodule)

    args = parser.parse_args()

    # Call subfunction with parsed arguments.
    args.func(args)

    return

if __name__ == '__main__':
    main()
