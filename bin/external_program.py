#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description='run a given python script')
parser.add_argument('--run-python', help='run a given python script')
args = parser.parse_args()


if args.run_python:
    try:
        s = subprocess.run(['python3', args.run_python], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as err:
        sys.exit(f"Calling {args.run_python} failed: {err.stderr}")
    else:
        print(s.stdout)
