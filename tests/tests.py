# bibliometrics: Summarize your Google Scholar bibliometrics in an SVG with GitHub Actions.
# 
# Copyright (c) 2022 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 


import unittest

import sys
sys.path.insert(0,'src')
import bibliometrics as bib

class TestSomething(unittest.TestCase) :

    def test_parse(self) :
        with open("tests/testcase.html.txt", "r") as f :
            page = f.read().replace('\n', '')
            metrics = bib.parseBibliometrics(page)
            self.assertEqual("2052", metrics["total"])
            self.assertEqual("364", metrics["fiveYear"])
            self.assertEqual("25", metrics["h"])
            self.assertEqual("33", metrics["i10"])
            print(metrics)

    def test_anothertestcase(self) :
        pass
