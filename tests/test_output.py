import contextlib
import io
import unittest

from austin.output import output

INFO = {
    'contributors': {
        'top': [
            ['spiderman', 42],
            ['batman', 27],
        ]
    },
    'pulls': {
        'open_count': 1,
        'closed_count': 2,
        'stale_count': 3,
    },
    'issues': {
        'open_count': 1,
        'closed_count': 2,
        'stale_count': 3,
    }
}
EXPECTED_STDOUT = 'Top contributors:\n+----+-----------------+---------+\n| #  | login           | commits |\n+----+-----------------+---------+\n| 1  | spiderman       | 42      |\n| 2  | batman          | 27      |\n+----+-----------------+---------+\n\nOpen pull requests count: 1\nClosed pull requests count: 2\nStale pull requests count: 3\n\nOpen issues count: 1\nClosed issues count: 2\nStale issues count: 3\n'


class TestOutput(unittest.TestCase):
    def test_output(self):
        with io.StringIO() as buffer:
            with contextlib.redirect_stdout(buffer):
                output(INFO)
            stdout = buffer.getvalue()

        self.assertEqual(stdout, EXPECTED_STDOUT)
