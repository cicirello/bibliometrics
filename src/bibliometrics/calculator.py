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

import math

class BibliometricCalculator:
    """Calculates the various bibliometrics."""

    __slots__ = [ '_metrics' ]

    def __init__(self, metrics, cites_list):
        """Initializes the BibliometricCalculator.

        Keyword arguments:
        metrics - a dict of the metrics scraped directly from Scholar profile
        cites_list - a list of the citations of articles scraped from profile
        """
        self._metrics = dict(metrics)
        if "h-index" not in self._metrics or len(cites_list) == 0:
            return
        sorted_cites = sorted(cites_list, reverse=True)
        if sorted_cites[0] <= 0:
            return
        self._calculate_most(sorted_cites)
        self._calculate_o_index()
        self._calculate_g_index(sorted_cites)
        self._calculate_h_median(sorted_cites)
        h_core_sum = self._calculate_h_core_citations(sorted_cites)
        self._calculate_e_index(h_core_sum)
        self._calculate_R_index(h_core_sum)
        self._calculate_A_index(h_core_sum)
        self._calculate_ixx_index(sorted_cites, 100)
        self._calculate_ixx_index(sorted_cites, 1000)
        self._calculate_ixx_index(sorted_cites, 10000)
        self._calculate_w_index(sorted_cites)

    def to_dict(self):
        """Returns a dict of the bibliometrics."""
        return dict(self._metrics)

    def _calculate_most(self, sorted_cites):
        """Initializes the most cited.

        Keyword arguments:
        sorted_cites - a list of the citations per publication sorted decreasing
        """
        self._metrics["most-cited"] = sorted_cites[0]

    def _calculate_o_index(self):
        """Calculates the o-index, which is the geometric mean
        of the h-index and the number of citations to the most-cited
        paper.
        """
        if "most-cited" in self._metrics:
            self._metrics["o-index"] = round(
                math.sqrt(
                    self._metrics["h-index"] * self._metrics["most-cited"]
                )
            )

    def _calculate_g_index(self, sorted_cites) :
        """Calculates the g-index.

        Keyword arguments:
        sorted_cites - List of citations of papers in decreasing order.
        """
        rolling_sum = [ sorted_cites[0] ]
        for i in range(1, len(sorted_cites)) :
            rolling_sum.append(sorted_cites[i] + rolling_sum[i-1])
        rolling_sum = [ (i+1, x) for i, x in enumerate(rolling_sum) ]
        g = max(y for y, x in rolling_sum if x >= y*y)
        if g > 0 and g < 100 :
            self._metrics["g-index"] = g

    def _calculate_h_median(self, sorted_cites) :
        """Calculates the median number of citations to publications in
        the h-core, i.e., the h most-cited papers.

        Keyword arguments:
        sorted_cites - List of citations of papers in decreasing order.
        """
        h = self._metrics["h-index"]
        if h >= 200:
            return
        if h % 2 == 0:
            m1 = h // 2
            if m1 >= len(sorted_cites):
                return
            m0 = m1 - 1
            total = sorted_cites[m0] + sorted_cites[m1]
            median = total // 2 if total % 2 == 0 else total / 2
        else:
            m = h // 2
            median = sorted_cites[m] if m < len(sorted_cites) else 0
        if median > 0.0:
            self._metrics["h-median"] = median if (
                isinstance(median, int)) else "{0:.1f}".format(median)

    def _calculate_h_core_citations(self, sorted_cites) :
        """Calculates the total number of citations to the publications
        in the h-core, i.e., the h most-cited papers.

        Keyword arguments:
        sorted_cites - List of citations of papers in decreasing order.
        """
        if self._metrics["h-index"] > 100:
            return 0
        if len(sorted_cites) < self._metrics["h-index"]:
            return 0
        return sum(sorted_cites[i] for i in range(self._metrics["h-index"]))

    def _calculate_e_index(self, h_core_sum) :
        """Calculates the e-index.

        Keyword arguments:
        h_core_sum - sum of the citations to the h publications in the h-core.
        """
        h = self._metrics["h-index"]
        e = math.sqrt(h_core_sum - h*h) if h <= 100 else 0
        if e > 0.0 :
            self._metrics["e-index"] = "{0:.2f}".format(e)

    def _calculate_R_index(self, h_core_sum) :
        """Calculates the R-index.

        Keyword arguments:
        h_core_sum - sum of the citations to the h publications in the h-core.
        """
        r = math.sqrt(h_core_sum) if self._metrics["h-index"] <= 100 else 0
        if r > 0.0 :
            self._metrics["r-index"] = "{0:.2f}".format(r)

    def _calculate_A_index(self, h_core_sum) :
        """Calculates the A-index.

        Keyword arguments:
        h_core_sum - sum of the citations to the h publications in the h-core.
        """
        h = self._metrics["h-index"]
        a = h_core_sum / h if h > 0 and h <= 100 else 0
        if a > 0.0 :
            self._metrics["a-index"] = "{0:.2f}".format(a)

    def _calculate_ixx_index(self, sorted_cites, xx):
        """Calculates i100, i1000, etc.

        Keyword arguments:
        sorted_cites - List of citations of papers in decreasing order.
        xx - 100 for i100-index, 1000 for i1000-index, etc.
        """
        ixx = sum(1 for y in sorted_cites if y >= xx)
        if ixx > 0 and ixx < 100:
            self._metrics["i{0}-index".format(xx)] = ixx

    def _calculate_w_index(self, sorted_cites):
        """Calculates the w-index.

        Keyword arguments:
        sorted_cites - List of citations of papers in decreasing order.
        """
        w = sum(1 for i, c in enumerate(sorted_cites) if c >= 10*(i+1))
        if w > 0 and w < 100:
            self._metrics["w-index"] = w

