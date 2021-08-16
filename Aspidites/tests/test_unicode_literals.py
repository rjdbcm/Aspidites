# encoding: utf-8
from Aspidites._vendor.contracts import contract
from Aspidites._vendor.contracts.main import parse_contract_string
from Aspidites._vendor.contracts.library import Extension
name = 'helló wörld from one'

import unittest

class TestParsingNumbers(unittest.TestCase):

    def test_unicode_literal(self):
        r = parse_contract_string(u'int')
        assert r == Extension('int')

    def test_unicode_literal2(self):

        @contract(x='string')
        def f(x):
            pass


        f('')
