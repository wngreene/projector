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
import re
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

    # Add a gitmodules.
    with open(join(args.path, ".gitmodules"), "w") as gitmodules:
        pass

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

    working_dir = os.getcwd()
    repo = Repo(working_dir)
    relpath = os.path.relpath(repo.working_dir, working_dir)
    sm_name = re.split('[\./]', args.url)[-2]

    # Add submodule.
    print GREEN + "Adding submodule:"
    print BLUE + "  git submodule add %s %s" % (args.url, os.path.join(relpath, sm_name))

    sm = repo.create_submodule(sm_name, os.path.join(sm_name),
                               url=args.url, branch="master")

    # Make add_submodule call in CMakeLists.
    with open(os.path.join(repo.working_dir, "CMakeLists.txt"), 'a') as cml:
        cmd = "add_submodule(%s DIRECTORY ./%s" % (sm_name, sm_name)

        if args.depends is not None:
            cmd += " DEPENDS"
            for dep in args.depends:
                cmd += " %s" % dep

        cmd += ")"

        print BLUE + "  echo \"%s\" >> %s/CMakeLists.txt" % (cmd, relpath)
        cml.write(cmd)

    # Stage change.
    repo.index.add(["CMakeLists.txt"])

    # Commit changes.
    # TODO(wng): Should this be automatically commited?
    # Leaving commented out for now.
    # print BLUE + "  git commit -m \"Added submodule %s\"" % sm_name
    # repo.index.commit("Added submodule %s." % sm_name)

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
    add_parser.add_argument('-d', '--depends', nargs='*', help='Project dependencies.')
    add_parser.set_defaults(func=add_submodule)

    args = parser.parse_args()

    # Call subfunction with parsed arguments.
    args.func(args)

    return

if __name__ == '__main__':
    main()
