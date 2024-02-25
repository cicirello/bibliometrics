# bibliometrics: Summarize your Google Scholar bibliometrics in an SVG
# 
# Copyright (c) 2022-2024 Vincent A Cicirello
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
from bibliometrics.calculator import BibliometricCalculator

class TestBibiometrics(unittest.TestCase) :

    # To have tests generate sample images (to files),
    # change this to True.
    printSampleImage = False

    def test_calculator_retains_scraped(self):
        metrics = {
            "total-cites" : 42,
            "five-year-cites" : 6,
            "h-index" : 3,
            "i10-index" : 1
        }
        calc = BibliometricCalculator(metrics, [])
        self.assertEqual(metrics, calc._metrics)
        calc = BibliometricCalculator(metrics, [5, 20, 9])
        for key, value in metrics.items():
            self.assertEqual(value, calc._metrics[key])

    def test_calculate_most(self):
        metrics = {
            "total-cites" : 42,
            "five-year-cites" : 6,
            "h-index" : 3,
            "i10-index" : 1
        }
        calc = BibliometricCalculator(metrics, [5, 20, 9])
        self.assertEqual(20, calc._metrics["most-cited"])

    def test_calculate_o_index(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        self.assertEqual(42, BibliometricCalculator(metrics, [42]*42)._metrics["o-index"])
        metrics["h-index"] = 1
        self.assertEqual(8, BibliometricCalculator(metrics, [5, 20, 64])._metrics["o-index"])
        metrics["h-index"] = 2
        self.assertEqual(8, BibliometricCalculator(metrics, [5, 20, 32])._metrics["o-index"])
        metrics["h-index"] = 0
        self.assertEqual(0, BibliometricCalculator(metrics, [1, 0, 2])._metrics["o-index"])

    def test_calculate_g(self) :
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 1,
            "i10-index" : 1
        }
        for g in range(1, 11) :
            cites = [10]*g
            self.assertEqual(g, BibliometricCalculator(metrics, cites)._metrics["g-index"])
        for g in range(11, 21) :
            cites = [10]*g
            self.assertEqual(10, BibliometricCalculator(metrics, cites)._metrics["g-index"])        

    def test_calculate_h_median(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        cites = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
        expected= [
            30, 29.5, 29, 28.5, 28, 27.5, 27, 26.5, 26,
            25.5, 25, 24.5, 24, 23.5, 23, 22.5, 22, 21.5, 21, 20.5]
        for i in range(len(expected)):
            metrics["h-index"] = i + 1
            if expected[i] > 0:
                h_median = BibliometricCalculator(metrics, cites)._metrics["h-median"]
                self.assertEqual(
                    expected[i],
                    float(h_median) if isinstance(h_median, str) else h_median
                )
            else:
                self.assertFalse("h-median" in BibliometricCalculator(metrics, cites)._metrics)
    
    def test_calculate_h_core_citations(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        cites = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
        for h in range(1, 1+len(cites)):
            metrics["h-index"] = h
            expected = 10 * (55 - (10-h)*(11-h)//2)
            self.assertEqual(
                expected,
                BibliometricCalculator(metrics, cites)._calculate_h_core_citations(cites)
            )

    def test_calculate_e_no_excess(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        for h in range(0, 10) :
            metrics["h-index"] = h
            cites = [h]*20
            self.assertFalse("e-index" in BibliometricCalculator(metrics, cites)._metrics)
            
    def test_calculate_e_equal_excess(self) :
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        for h in range(1, 10) :
            metrics["h-index"] = h
            cites = [h+5]*h + [1]*5
            self.assertAlmostEqual(
                math.sqrt(5*h),
                float(BibliometricCalculator(metrics, cites)._metrics["e-index"]),
                places=2
            )

    def test_calculate_e_unequal_excess(self) :
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        for h in range(1, 10) :
            metrics["h-index"] = h
            cites = [h+x for x in range(h, 0, -1)]
            self.assertAlmostEqual(
                math.sqrt(h*(h+1)/2),
                float(BibliometricCalculator(metrics, cites)._metrics["e-index"]),
                places=2
            )

    def test_calculate_R_index(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        inputs = [100, 81, 64, 4, 1]
        outputs = [10, 9, 8, 2, 1]
        for h_core_sum, expected in zip(inputs, outputs):
            metrics["h-index"] = 1
            cites = [h_core_sum] + [0]*5
            self.assertEqual(
                expected,
                float(BibliometricCalculator(metrics, cites)._metrics["r-index"])
            )

    def test_calculate_A_index(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 42,
            "i10-index" : 1
        }
        h_core_sum = 100
        inputs = [1, 2, 4, 5]
        outputs = [100, 50, 25, 20]
        for h, expected in zip(inputs, outputs):
            metrics["h-index"] = h
            cites = [h_core_sum // h]*h + [0]*5
            self.assertEqual(
                expected,
                float(BibliometricCalculator(metrics, cites)._metrics["a-index"])
            )

    def test_calculate_ixx_index(self):
        metrics = {
            "total-cites" : 4200,
            "five-year-cites" : 6,
            "h-index" : 9,
            "i10-index" : 1
        }
        cites = [10001, 10000, 1002, 1001, 1000, 103, 102, 101, 100, 5, 4, 3, 2, 1]
        calc = BibliometricCalculator(metrics, cites)
        self.assertEqual(2, calc._metrics["i10000-index"])
        self.assertEqual(5, calc._metrics["i1000-index"])
        self.assertEqual(9, calc._metrics["i100-index"])

    def test_parse(self) :
        with open("tests/testcase.html.txt", "r") as f :
            page = f.read().replace('\n', '')
            metrics = bib.parseBibliometrics(page)
            self.assertEqual(2052, metrics["total-cites"])
            self.assertEqual(364, metrics["five-year-cites"])
            self.assertEqual(25, metrics["h-index"])
            self.assertEqual(33, metrics["i10-index"])
            self.assertEqual(44, metrics["g-index"])
            self.assertEqual(228, metrics["most-cited"])
            self.assertEqual(3, metrics["i100-index"])
            self.assertEqual(75, metrics["o-index"])
            self.assertEqual(48, metrics["h-median"])
            self.assertEqual("34.12", metrics["e-index"])
            self.assertEqual("42.30", metrics["r-index"])
            self.assertEqual("71.56", metrics["a-index"])
            self.assertFalse("i1000-index" in metrics)
            self.assertFalse("i10000-index" in metrics)

    def test_generate_image(self) :
        metrics = {
            "total-cites" : 2052,
            "five-year-cites" : 364,
            "h-index" : 25,
            "i10-index" : 33,
            "i100-index" : 3,
            "g-index" : 44,
            "most-cited" : 228,
            "o-index" : 75,
            "h-median" : 48,
            "e-index" : "34.12",
            "r-index" : "42.30",
            "a-index" : "71.56"
        }
        stats = [
            "total-cites",
            "five-year-cites",
            "most-cited",
            "h-index",
            "g-index",
            "i10-index",
            "i100-index",
            "i1000-index",
            "i10000-index",
            "o-index",
            "h-median",
            "e-index",
            "r-index",
            "a-index"
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
