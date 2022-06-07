#!/usr/bin/env -S python3 -B
#
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

import sys, math
from TextLength import calculateTextLength, calculateTextLength110Weighted

template = """<svg width="{0}" height="{1}" viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg" lang="en" xml:lang="en">
<rect x="{2}" y="{2}" stroke-width="{3}" rx="{4}" width="{5}" height="{6}" stroke="{7}" fill="{8}"/>
<g font-weight="600" font-size="110pt" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision">
{9}
{10}
{11}
{12}
{13}
{14}
</g></g></svg>
"""

titleTemplate = """<text x="{0}" y="{1}" lengthAdjust="spacingAndGlyphs" textLength="{2}" transform="scale({3})" fill="{4}">{5}</text>
<g fill="{6}">"""

metricTemplate = """<g transform="translate({0}, {1})">
<g transform="scale({2})">
<text lengthAdjust="spacingAndGlyphs" textLength="{3}" x="{4}" y="{5}">{6}</text>
<text lengthAdjust="spacingAndGlyphs" textLength="{7}" x="{8}" y="{5}">{9}</text>
</g></g>"""

def generateBibliometricsImage(metrics, colors, titleText) :
    """Generates the bibliometrics image as an SVG.

    Keyword arguments:
    metrics - dictionary with the stats
    colors - dictionary with colors
    """
    titleSize = 18
    textSize = 14
    margin = 15
    scale = round(0.75 * titleSize / 110, 3)
    stroke = 4
    radius = 6
    lineHeight = 21
    
    titleLength = round(calculateTextLength110Weighted(titleText, 600))
    minWidth = calculateTextLength(titleText, titleSize, True, 600) + 2*margin
    minHeight = 39
    title = titleTemplate.format(
        str(round(margin/scale)),  #0  x
        str(round(37/scale)),  #1  y
        titleLength,  #2
        "{0:.3f}".format(scale), #3
        colors["title"], #4
        titleText,  #5
        colors["text"] #6
    )

    minWidth = max(minWidth, 2 * calculateTextLength("Total citations", textSize, True, 600) + 2*margin)
    minWidth = max(minWidth, 2 * calculateTextLength("Five-year citations", textSize, True, 600) + 2*margin)
    minWidth = max(minWidth, 2 * calculateTextLength("h-index", textSize, True, 600) + 2*margin)
    minWidth = max(minWidth, 2 * calculateTextLength("i10-index", textSize, True, 600) + 2*margin)
    minWidth = max(minWidth, 2 * calculateTextLength("g-index", textSize, True, 600) + 2*margin)

    offset = minHeight + lineHeight
    minHeight += lineHeight
    scale = round(0.75 * textSize / 110, 3)

    label = "Total citations"
    data = str(metrics["total"])
    totalCites = metricTemplate.format(
        margin,
        offset,
        scale,
        round(calculateTextLength110Weighted(label, 600)),
        0,
        round(12.5/scale),
        label,
        round(calculateTextLength110Weighted(data, 600)),
        round(minWidth/2/scale),
        data
    )

    offset += lineHeight
    minHeight += lineHeight
    label = "Five-year citations"
    data = str(metrics["fiveYear"])
    fiveYearCites = metricTemplate.format(
        margin,
        offset,
        scale,
        round(calculateTextLength110Weighted(label, 600)),
        0,
        round(12.5/scale),
        label,
        round(calculateTextLength110Weighted(data, 600)),
        round(minWidth/2/scale),
        data
    )

    offset += lineHeight
    minHeight += lineHeight
    label = "h-index"
    data = str(metrics["h"])
    h = metricTemplate.format(
        margin,
        offset,
        scale,
        round(calculateTextLength110Weighted(label, 600)),
        0,
        round(12.5/scale),
        label,
        round(calculateTextLength110Weighted(data, 600)),
        round(minWidth/2/scale),
        data
    )

    offset += lineHeight
    minHeight += lineHeight
    label = "i10-index"
    data = str(metrics["i10"])
    i10 = metricTemplate.format(
        margin,
        offset,
        scale,
        round(calculateTextLength110Weighted(label, 600)),
        0,
        round(12.5/scale),
        label,
        round(calculateTextLength110Weighted(data, 600)),
        round(minWidth/2/scale),
        data
    )

    offset += lineHeight
    minHeight += lineHeight
    label = "g-index"
    data = str(metrics["g"])
    g = metricTemplate.format(
        margin,
        offset,
        scale,
        round(calculateTextLength110Weighted(label, 600)),
        0,
        round(12.5/scale),
        label,
        round(calculateTextLength110Weighted(data, 600)),
        round(minWidth/2/scale),
        data
    )

    minHeight += 2 * lineHeight
    minWidth = math.ceil(minWidth)
    image = template.format(
        minWidth,  #0
        minHeight, #1
        stroke//2, #2
        stroke, #3   
        radius,  #4  
        minWidth - stroke,  #5 rect width
        minHeight - stroke,   #6 rect height
        colors["border"],  #7
        colors["background"],  #8
        title, #9
        totalCites, #10
        fiveYearCites, #11
        h, #12
        i10, #13
        g #14
    )
    return image

def parseBibliometrics(page) :
    """Parses a Scholar Profile for the bibliometrics.

    Keyword arguments:
    page - The user profile page
    """
    metrics = {}
    i = page.find("</td>")
    if i < 0 :
        return metrics
    i += 5
    endStat = page.find("</td>", i)
    if endStat < 0 :
        return metrics
    startStat = page.rfind(">", i, endStat)
    if startStat < 0 :
        return metrics
    totalCitations = page[startStat+1:endStat]
    metrics["total"] = int(totalCitations.strip())
    i = endStat + 6
    endStat = page.find("</td>", i)
    if endStat < 0 :
        return metrics
    i += 5
    startStat = page.rfind(">", i, endStat)
    if startStat < 0 :
        return metrics
    fiveYearCitations = page[startStat+1:endStat]
    metrics["fiveYear"] = int(fiveYearCitations.strip())
    i = endStat + 6
    i = page.find("</td>", i+1)
    if i < 0 :
        return metrics
    endStat = page.find("</td>", i+1)
    if endStat < 0 :
        return metrics
    i += 5
    startStat = page.rfind(">", i, endStat)
    if startStat < 0 :
        return metrics
    h = page[startStat+1:endStat]
    metrics["h"] = int(h.strip())
    i = endStat + 6
    i = page.find("</td>", i+1)
    if i < 0 :
        return metrics
    i = i + 6
    i = page.find("</td>", i+1)
    if i < 0 :
        return metrics
    endStat = page.find("</td>", i+1)
    if endStat < 0 :
        return metrics
    i += 5
    startStat = page.rfind(">", i, endStat)
    if startStat < 0 :
        return metrics
    i10 = page[startStat+1:endStat]
    metrics["i10"] = int(i10.strip())
    g = calculateG(page)
    if g > 0 :
        metrics["g"] = g
    return metrics

def calculateG(page) :
    """Calculates the g-index.

    Keyword arguments:
    page - The user profile page
    """
    citesList = parseDataForG(page)
    if len(citesList) > 0 :
        citesList.sort(reverse=True)
        for i in range(1, len(citesList)) :
            citesList[i] = citesList[i] + citesList[i-1]
        citesList = [ (i+1, x) for i, x in enumerate(citesList) ]
        return max(y for y, x in citesList if x >= y*y)
    return 0
    

def parseDataForG(page) :
    """Parses the cites per publication for calculating g-index

    Keyword arguments:
    page - The user profile page
    """
    marker = "class=\"gsc_a_ac gs_ibl\">"
    citesList = []
    nextLeft = page.find(marker)
    while nextLeft >= 0 :
        nextLeft += len(marker)
        right = page.find("</a>", nextLeft)
        if right >= 0 :
            cites = page[nextLeft:right].strip()
            if len(cites) > 0 :
                citesList.append(int(cites))
        else :
            right = nextLeft + 1
        nextLeft = page.find(marker, right)
    return citesList

if __name__ == "__main__" :
    # Rename these variables to something meaningful
    input1 = sys.argv[1]
    input2 = sys.argv[2]


    # Fake example outputs
    output1 = "Hello"
    output2 = "World"

    # This is how you produce outputs.
    # Make sure corresponds to output variable names in action.yml
    print("::set-output name=output-one::" + output1)
    print("::set-output name=output-two::" + output2)
