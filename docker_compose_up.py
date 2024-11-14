#!/usr/bin/env python3

import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--up", action="store_true", help="start docker-compose"
    )
    parser.add_argument(
        "-d", "--down", action="store_true", help="stop docker-compose"
    )
    args = parser.parse_args()

    if args.up and args.down:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not (args.up or args.down):
        parser.print_help(sys.stderr)
        sys.exit(1)

    os.chdir("/media/mix060514/EE9E67E99E67A933/pj/finmind")
    if args.up:
        os.system("docker compose -f mysql.yml up -d")
    else:
        os.system("docker compose -f mysql.yml down")

if __name__ == "__main__":
    main()

