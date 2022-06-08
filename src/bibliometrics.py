#!/usr/bin/env -S python3 -B
#
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

import sys, math, os
from datetime import date
from TextLength import calculateTextLength, calculateTextLength110Weighted

template = """<svg width="{0}" height="{1}" viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg" lang="en" xml:lang="en">
<rect x="{2}" y="{2}" stroke-width="{3}" rx="{4}" width="{5}" height="{6}" stroke="{7}" fill="{8}"/>
<g font-weight="600" font-size="110pt" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision">
{9}
{10}
{11}
</g></g></svg>
"""

titleTemplate = """<text x="{0}" y="{1}" lengthAdjust="spacingAndGlyphs" textLength="{2}" transform="scale({3})" fill="{4}">{5}</text>
<g fill="{6}">"""

metricTemplate = """<g transform="translate({0}, {1})">
<g transform="scale({2})">
<text lengthAdjust="spacingAndGlyphs" textLength="{3}" x="{4}" y="{5}">{6}</text>
<text lengthAdjust="spacingAndGlyphs" textLength="{7}" x="{8}" y="{5}">{9}</text>
</g></g>"""

lastUpdatedTemplate = """<g transform="translate({0}, {1})">
<g transform="scale({2})">
<text lengthAdjust="spacingAndGlyphs" textLength="{3}" x="{4}" y="{5}">{6}</text>
</g></g>"""

def generateBibliometricsImage(metrics, colors, titleText) :
    """Generates the bibliometrics image as an SVG.

    Keyword arguments:
    metrics - dictionary with the stats
    colors - dictionary with colors
    """
    titleSize = 20
    titleLineHeight = 2 * titleSize + 1
    textSize = 16
    smallSize = 12
    margin = 15
    scale = round(0.75 * titleSize / 110, 3)
    stroke = 4
    radius = 6
    lineHeight = round(textSize * 1.5)
    drop = round(textSize * 12.5 / 14, 1)

    stats = [
        ("Total citations", "total"),
        ("Five-year citations", "fiveYear"),
        ("h-index", "h"),
        ("i10-index", "i10"),
        ("g-index", "g"),
        ("Most-cited paper", "most")
    ]

    lastUpdatedText = "Last updated: " + date.today().strftime("%d %B %Y")
    lastUpdatedLength = calculateTextLength(lastUpdatedText, smallSize, True, 600)
    
    titleLength = round(calculateTextLength110Weighted(titleText, 600))
    minWidth = calculateTextLength(titleText, titleSize, True, 600) + 2*margin
    minWidth = max(minWidth, lastUpdatedLength + 2*margin)
    for label, key in stats :
        minWidth = max(minWidth, 2 * calculateTextLength(label, textSize, True, 600) + 2*margin)
    minWidth = math.ceil(minWidth)

    minHeight = titleLineHeight + 2
    centered = round((minWidth / 2)/scale - titleLength / 2)
    title = titleTemplate.format(
        centered, #round(margin/scale),  #0  x
        round(titleLineHeight/scale),  #1  y
        titleLength,  #2
        "{0:.3f}".format(scale), #3
        colors["title"], #4
        titleText,  #5
        colors["text"] #6
    )
    offset = minHeight
    scale = round(0.75 * textSize / 110, 3)

    formattedStats = []
    for label, key in stats :
        if key in metrics :
            offset += lineHeight
            minHeight += lineHeight
            data = str(metrics[key])
            dataWidthPreScale = round(calculateTextLength110Weighted(data, 600))
            entry = metricTemplate.format(
                margin,
                offset,
                scale,
                round(calculateTextLength110Weighted(label, 600)),
                0,
                round(drop/scale),
                label,
                dataWidthPreScale,
                round((minWidth - 2*margin)/scale) - dataWidthPreScale,   #round(minWidth/2/scale),
                data
            )
            formattedStats.append(entry)

    scale = round(0.75 * smallSize / 110, 3)

    offset += 2*lineHeight
    minHeight += 2*lineHeight
    lastUpdated = lastUpdatedTemplate.format(
        margin,
        offset,
        scale,
        round(lastUpdatedLength/scale),
        0,
        round(round(smallSize * 12.5 / 14, 1)/scale),
        lastUpdatedText
    )

    minHeight += lineHeight
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
        ''.join(formattedStats), #10
        lastUpdated #11
    )
    return image.replace("\n", "")

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
    g, most = calculateMostAndG(page)
    if g > 0 :
        metrics["g"] = g
    if most > 0 :
        metrics["most"] = most
    return metrics

def calculateMostAndG(page) :
    """Calculates the g-index and the most cited paper.

    Keyword arguments:
    page - The user profile page
    """
    citesList = parseDataForG(page)
    if len(citesList) > 0 :
        citesList.sort(reverse=True)
        most = citesList[0]
        for i in range(1, len(citesList)) :
            citesList[i] = citesList[i] + citesList[i-1]
        citesList = [ (i+1, x) for i, x in enumerate(citesList) ]
        return max(y for y, x in citesList if x >= y*y), most
    return 0, 0
    
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

def outputImage(image, filename) :
    """Outputs the SVG to a file.

    Keyword arguments:
    image - The SVG as a string
    filename - The filename with path
    """
    # Create the directory if it doesn't exist.
    directoryName = os.path.dirname(filename)
    if len(directoryName) > 0 :
        os.makedirs(directoryName, exist_ok=True, mode=0o777)
    try:
        # Write the image to a file
        with open(filename, "wb") as file:
            image = image.encode(encoding="UTF-8")
            file.write(image)
    except IOError:
        print("Error: An error occurred while writing the image to a file.")
        exit(1)

if __name__ == "__main__" :

    metrics = {
        "total" : 2052,
        "fiveYear" : 364,
        "h" : 25,
        "i10" : 33,
        "g" : 44,
        "most" : 228
    }

    configuration = {
        "jsonOutputFile" : ".bibliometrics.json",
        "svgConfig" : [
            {
                "filename" : "images/bibliometrics2.svg",
                "title" : "#58a6ff",
                "border" : "rgba(56,139,253,0.4)",
                "background" : "#010409",
                "text" : "#c9d1d9"
            },
            {
                "filename" : "images/bibliometrics.svg",
                "title" : "#862d2d",
                "border" : "#862d2d",
                "background" : "#f6f0bb",
                "text" : "#305030"
            }
        ]
    }


    for colors in configuration["svgConfig"] :
        image = generateBibliometricsImage(
            metrics,
            colors,
            "Bibliometrics"
        )
        outputImage(image, colors["filename"])
    
    


