# bibliometrics: Summarize your Google Scholar bibliometrics in an SVG
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

import sys, math
sys.path.insert(0,'src')
import bibliometrics.bibliometrics as bib

class TestBibiometrics(unittest.TestCase) :

    # To have tests generate sample images (to files),
    # change this to True.
    printSampleImage = False

    def test_calculate_h_core_citations(self):
        cites = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        for h in range(1, 1+len(cites)):
            expected = 55 - (10-h)*(11-h)//2
            self.assertEqual(expected, bib.calculate_h_core_citations(cites, h))

    def test_calculate_g(self) :
        for g in range(1, 11) :
            cites = [10]*g
            self.assertEqual(g, bib.calculate_g_index(cites))
        for g in range(11, 21) :
            cites = [10]*g
            self.assertEqual(10, bib.calculate_g_index(cites))

    def test_calculate_e_no_excess(self) :
        for h in range(0, 10) :
            h_core_sum = h*h
            self.assertEqual(0.0, bib.calculate_e_index(h_core_sum, h))

    def test_calculate_e_equal_excess(self) :
        for h in range(0, 10) :
            h_core_sum = h*h + 5*h
            self.assertEqual(math.sqrt(5*h), bib.calculate_e_index(h_core_sum, h))

    def test_calculate_e_unequal_excess(self) :
        for h in range(0, 10) :
            h_core_sum = sum(h+x for x in range(h, 0, -1))
            self.assertEqual(math.sqrt(h*(h+1)/2), bib.calculate_e_index(h_core_sum, h))

    def test_parse(self) :
        with open("tests/testcase.html.txt", "r") as f :
            page = f.read().replace('\n', '')
            metrics = bib.parseBibliometrics(page)
            self.assertEqual(2052, metrics["total"])
            self.assertEqual(364, metrics["fiveYear"])
            self.assertEqual(25, metrics["h"])
            self.assertEqual(33, metrics["i10"])
            self.assertEqual(44, metrics["g"])
            self.assertEqual(228, metrics["most"])
            self.assertEqual(3, metrics["i100"])
            self.assertEqual("34.12", metrics["e"])
            self.assertFalse("i1000" in metrics)
            self.assertFalse("i10000" in metrics)

    def test_generate_image(self) :
        metrics = {
            "total" : 2052,
            "fiveYear" : 364,
            "h" : 25,
            "i10" : 33,
            "i100" : 3,
            "g" : 44,
            "most" : 228,
            "e" : "34.12"
        }
        stats = [
            "total",
            "fiveYear",
            "most",
            "h",
            "g",
            "i10",
            "i100",
            "i1000",
            "i10000",
            "e"
        ]
        colors = {
            "title" : "#58a6ff",
            "border" : "rgba(56,139,253,0.4)",
            "background" : "#010409",
            "text" : "#c9d1d9"
        }
        image = bib.generateBibliometricsImage(
            metrics,
            colors,
            "Bibliometrics",
            stats
        )
        colors2 = {
            "background": "#f6f8fa",
            "border": "rgba(84,174,255,0.4)",
            "text": "#24292f",
            "title": "#0969da"
        }
        image2 = bib.generateBibliometricsImage(
            metrics,
            colors2,
            "Bibliometrics",
            stats
        )
        if TestBibiometrics.printSampleImage :
            bib.outputImage(image, "images/bibliometrics2.svg")
            bib.outputImage(image2, "images/bibliometrics.svg")
            bib.outputJSON("bibliometrics.json", metrics)
