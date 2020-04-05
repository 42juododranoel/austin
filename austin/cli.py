import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('url')
    parser.add_argument('--branch', default='master')
    parser.add_argument('--start-date', help='YYYY-MM-DD')
    parser.add_argument('--end-date', help='YYYY-MM-DD')

    return parser
