'''Tests for shared normalization helpers'''
from pyairnow.util import coalesce


class TestCoalesce:
    def test_returns_first_present_value(self):
        assert coalesce({'a': 1, 'b': 2}, 'a', 'b') == 1

    def test_skips_null_value(self):
        assert coalesce({'a': None, 'b': 2}, 'a', 'b') == 2

    def test_skips_absent_key(self):
        assert coalesce({'b': 2}, 'a', 'b') == 2

    def test_default_when_all_null(self):
        assert coalesce({'a': None, 'b': None}, 'a', 'b', default='x') == 'x'

    def test_default_when_all_absent(self):
        assert coalesce({}, 'a', 'b', default='x') == 'x'

    def test_default_is_none_when_unset(self):
        assert coalesce({}, 'a') is None

    def test_falsy_values_are_not_skipped(self):
        assert coalesce({'a': 0}, 'a', default=-1) == 0
        assert coalesce({'a': False}, 'a', default=True) is False
        assert coalesce({'a': ''}, 'a', default='x') == ''
