def print_horizontal_border():
    print('+----+-----------------+---------+')


def output(info):
    """Consume info and pretty print it"""

    print('Top contributors:')

    i = 1
    print_horizontal_border()
    print(f'| #  | {"login":<15} | {"commits":<7} |')
    print_horizontal_border()
    for contributor, commit_count in info['contributors']['top']:
        print(f'| {i:<2} | {contributor:<15} | {commit_count:<7} |')
        i += 1
    else:
        print_horizontal_border()
        print()

    print('Open pull requests count:', info['pulls']['open_count'])
    print('Closed pull requests count:', info['pulls']['closed_count'])
    print('Stale pull requests count:', info['pulls']['stale_count'])
    print()
    print('Open issues count:', info['issues']['open_count'])
    print('Closed issues count:', info['issues']['closed_count'])
    print('Stale issues count:', info['issues']['stale_count'])
