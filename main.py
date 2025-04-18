#!/usr/bin/env/python3

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="A To do application run in the command line")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    create_parser = subparsers.add_parser("create", help="Create Something")
    create_parser.add_argument("name", help="Name of thing to create")
    create_parser.add_argument("--type", choices=["type1", "type2"], default="type1", help="type of thing to create")

    read_parser = subparsers.add_parser("read", help="Read something")
    read_parser.add_argument("id", help="ID of the thing to read")
    read_parser.add_argument("--format", choices=["text", "json"], default="text", help="output format")

    #You can add any other update or delete commands here
    # ...

    args = parser.parse_args()

    if args.command is None;
        parser.print_help()
        sys.exit(1)

    if args.command == "create":
        result = create_something(args.name, args.type)