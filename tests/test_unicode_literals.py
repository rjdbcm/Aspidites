# encoding: utf-8
from __future__ import unicode_literals

from Aspidites.libraries.contracts import contract
from Aspidites.libraries.contracts.main import parse_contract_string
name = 'helló wörld from one'

import unittest

class TestParsingNumbers(unittest.TestCase):

    def test_unicode_literal(self):
        r = parse_contract_string(u'int')
        print(r)

    def test_unicode_literal2(self):

        @contract(x='string')
        def f(x):
            pass


        f('')
