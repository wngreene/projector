#!/usr/bin/env python

# Copyright 2015 Massachusetts Institute of Tech

"""
A convenience tool for creating metaprojects.

Usage:
  >> metaproject init my_project
  >> metaproject add <git url> <dependencies>
"""

import argparse

def initialize(args):
    """Initialize a metaproject."""
    print args.path
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
