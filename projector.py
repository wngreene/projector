#!/usr/bin/env python

# Copyright 2015 Massachusetts Institute of Technology.

"""
A convenience tool for creating projects.

Usage:
  >> projector.py init my_project
  >> projector.py init -n my_meta_project
  >> projector add <git url> <path> -d <dependencies>
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

MODULE_EXAMPLE_URL = "git@github.mit.edu:rrg/module_example.git"
MODULE_EXAMPLE_BRANCH = "feature_template"

PROJECT_EXAMPLE_URL = "git@github.mit.edu:rrg/project_example.git"
PROJECT_EXAMPLE_BRANCH = "feature_template"

def replace_string(fname, old, new):
    """Replace a string in a file."""
    contents = ""
    with open(fname, "r") as fo:
        contents = fo.read()

        contents = contents.replace(old, new)

    with open(fname, "w") as fo:
        fo.write(contents)

    return

def underscores_to_camel_case(under_scores):
    """Convert under_scores to CamelCase."""
    ssplit = under_scores.split("_")
    caps = [ss.capitalize() for ss in ssplit]
    camel_case = ""
    for c in caps:
        camel_case += c

    return camel_case

def replace_string_dir(dirname, old, new):
    """Replace a string in all files in a directory."""
    for dname, dirs, files in os.walk(dirname):
        for fname in files:
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
                s = s.replace(old, new)
                with open(fpath, "w") as f:
                    f.write(s)

def initialize(args):
    """Initialize a project."""

    join = os.path.join

    print GREEN + "Project destination:"
    print BLUE + "  %s" % args.path
    root_dir = os.path.dirname(os.path.realpath(__file__))

    src = ""
    if args.meta:
        # Clone project_example and checkout template branch.
        repo = Repo.clone_from(PROJECT_EXAMPLE_URL, args.path)
        repo.git.checkout(PROJECT_EXAMPLE_BRANCH)

        # Remove .git folder.
        shutil.rmtree(join(args.path, ".git"))

        # Rename metaproject in README.md.
        src_split = os.path.split(args.path)
        name = src_split[-1]
        replace_string_dir(args.path, "project_example", name)

    else:
        # Clone module_example and checkout template branch.
        repo = Repo.clone_from(MODULE_EXAMPLE_URL, args.path)
        repo.git.checkout(MODULE_EXAMPLE_BRANCH)

        # Remove .git folder.
        shutil.rmtree(join(args.path, ".git"))

        # Replace "module_example".
        src_split = os.path.split(args.path)
        name = src_split[-1]
        replace_string_dir(args.path, "module_example", name)

        # Replace "MODULE_EXAMPLE"
        replace_string_dir(args.path, "MODULE_EXAMPLE", name.upper())

        # Replace "ModuleExample"
        camel_case_str = underscores_to_camel_case(name)
        replace_string_dir(args.path, "ModuleExample", camel_case_str)

        # Rename some files.
        os.rename(join(args.path, "src", "module_example", "module_example.h"),
                  join(args.path, "src", "module_example", "%s.h" % name))
        os.rename(join(args.path, "src", "module_example", "module_example.cc"),
                  join(args.path, "src", "module_example", "%s.cc" % name))
        os.rename(join(args.path, "src", "module_example_main.cc"),
                  join(args.path, "src", "%s_main.cc" % name))
        os.rename(join(args.path, "test", "module_example_test.cc"),
                  join(args.path, "test", "%s_test.cc" % name))

        # Rename some folders.
        os.rename(join(args.path, "src", "module_example"),
                  join(args.path, "src", name))
        os.rename(join(args.path, "cmake", "templates", "module_exampleConfig.cmake.in"),
                  join(args.path, "cmake", "templates", "%sConfig.cmake.in" % name))
        os.rename(join(args.path, "cmake", "templates", "module_exampleConfigVersion.cmake.in"),
                  join(args.path, "cmake", "templates", "%sConfigVersion.cmake.in" % name))

    # Initialize repo.
    print GREEN + "Initializing repository:"
    print BLUE + "  git init %s" % args.path
    print BLUE + "  cd %s" % args.path
    print BLUE + "  git add ."
    print BLUE + "  git commit -m \"Initialize project.\""

    repo = Repo.init(args.path)
    repo.git.add(all=True)
    repo.index.commit("Initialize project.")

    return

def add_submodule(args):
    """Add a git submodule to project."""

    repo = Repo(os.getcwd())
    relpath = args.path #os.path.relpath(repo.working_dir, working_dir)
    sm_name = re.split('[\./]', args.url)[-2]

    # Add submodule.
    print GREEN + "Adding submodule:"
    print BLUE + "  git submodule add %s %s/" % (args.url, relpath)

    submod = repo.create_submodule(sm_name, os.path.join(repo.working_dir, relpath, sm_name),
                                   url=args.url, branch="master")

    # Make add_submodule call in CMakeLists.
    with open(os.path.join(repo.working_dir, "CMakeLists.txt"), 'a') as cml:
        cmd = "\nadd_submodule(%s DIRECTORY %s/%s" % (sm_name, relpath, sm_name)

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
    """Main entry point for projector."""

    # Parse args.
    parser = argparse.ArgumentParser(description="A convenience tool for creating projects.")
    subparsers = parser.add_subparsers(help='Sub-command help')

    # Parser for init command.
    init_parser = subparsers.add_parser('init', help='Initialize a project')
    init_parser.add_argument('-m', '--meta', action='store_true', help='Make this project a metaproject.')
    init_parser.add_argument('path', help='Path to project.')
    init_parser.set_defaults(func=initialize)

    # Parser for add command.
    add_parser = subparsers.add_parser('add', help='Add a git submodule to a project.')
    add_parser.add_argument('url', help='Git repository url')
    add_parser.add_argument('path', help='Path to submodule.')
    add_parser.add_argument('-d', '--depends', nargs='*', help='Project dependencies.')
    add_parser.set_defaults(func=add_submodule)

    args = parser.parse_args()

    # Call subfunction with parsed arguments.
    args.func(args)

    return

if __name__ == '__main__':
    main()
