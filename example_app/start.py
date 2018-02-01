import os

import sys

start_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(start_dir)
sys.path.append(start_dir)
from meeepo import start_server


def startup():
    scan_path = 'example_app/controllers'
    port = 8080
    start_server(scan_path, port)


if __name__ == '__main__':
    startup()
