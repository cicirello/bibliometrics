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

import sys
sys.path.insert(0,'src')
import bibliometrics as bib

class TestBibiometrics(unittest.TestCase) :

    # To have tests generate sample images (to files),
    # change this to True.
    printSampleImage = False

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

    def test_generate_image(self) :
        metrics = {
            "total" : 2052,
            "fiveYear" : 364,
            "h" : 25,
            "i10" : 33,
            "g" : 44,
            "most" : 228
        }
        colors = {
            "title" : "#58a6ff",
            "border" : "rgba(56,139,253,0.4)",
            "background" : "#010409",
            "text" : "#c9d1d9"
        }
        image = bib.generateBibliometricsImage(
            metrics,
            colors,
            "Bibliometrics"
        )
        colors2 = {
            "background": "#f6f0bb",
            "border": "#862d2d",
            "text": "#305030",
            "title": "#862d2d"
        }
        image2 = bib.generateBibliometricsImage(
            metrics,
            colors2,
            "Bibliometrics"
        )
        if TestBibiometrics.printSampleImage :
            bib.outputImage(image, "images/bibliometrics2.svg")
            bib.outputImage(image2, "images/bibliometrics.svg")
