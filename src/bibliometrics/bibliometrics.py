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

import sys, math, os, json
from datetime import date
from urllib.request import urlopen
from urllib.error import HTTPError
from .text_length import calculateTextLength, calculateTextLength110Weighted
from .calculator import BibliometricCalculator

template = """<svg width="{0}" height="{1}" viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg" lang="en" xml:lang="en">
<rect x="{2}" y="{2}" stroke-width="{3}" rx="{4}" width="{5}" height="{6}" stroke="{7}" fill="{8}"/>
<g font-weight="600" font-size="110pt" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision">
{9}
{10}
{11}
{12}
{13}
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

urlTemplate = "https://scholar.google.com/citations?user={0}&pagesize=100"

scholarLogoTemplate = """
<svg x="{0}" y="{1}" width="{2}" height="{2}" viewBox="0 0 512 512"><path fill="#4285f4" d="M256 411.12L0 202.667 256 0z"/><path fill="#356ac3" d="M256 411.12l256-208.453L256 0z"/><circle fill="#a0c3ff" cx="256" cy="362.667" r="149.333"/><path fill="#76a7fa" d="M121.037 298.667c23.968-50.453 75.392-85.334 134.963-85.334s110.995 34.881 134.963 85.334H121.037z"/></svg>
"""

def generateBibliometricsImage(metrics, colors, titleText, stats) :
    """Generates the bibliometrics image as an SVG.

    Keyword arguments:
    metrics - dictionary with the stats
    colors - dictionary with colors
    titleText - text for the title of the svg
    stats - a list of the keys of the metrics to include in the order to
        include them
    """
    stats = [ key for key in stats if key in metrics ]
    titleSize = 18
    titleLineHeight = 2 * titleSize + 1
    textSize = 14
    smallSize = 12
    margin = 15
    scale = round(0.75 * titleSize / 110, 3)
    stroke = 4
    radius = 6
    lineHeight = round(textSize * 1.5)
    drop = round(textSize * 12.5 / 14, 1)
    scholarLogoDimensions = 32

    stat_labels = {
        "total-cites" : "Total citations",
        "five-year-cites" : "Five-year citations",
        "most-cited" : "Most-cited paper",
        "h-index" : "h-index",
        "m-quotient" : "m-quotient",
        "g-index" : "g-index",
        "i10-index" : "i10-index",
        "i100-index" : "i100-index",
        "i1000-index" : "i1000-index",
        "i10000-index" : "i10000-index",
        "w-index" : "w-index", 
        "o-index" : "o-index",
        "h-median" : "h-median", 
        "e-index" : "e-index",
        "r-index" : "r-index",
        "a-index" : "a-index"
    }

    lastUpdatedText = "Last updated: " + date.today().strftime("%d %B %Y")
    lastUpdatedLength = calculateTextLength(
        lastUpdatedText,
        smallSize,
        True,
        600
    )
    
    titleLength = round(calculateTextLength110Weighted(titleText, 600))
    minWidth = calculateTextLength(
        titleText,
        titleSize,
        True,
        600) + 4*margin + 2*scholarLogoDimensions
    minWidth = max(minWidth, lastUpdatedLength + 2*margin)
    for key in stats :
        label = stat_labels[key]
        minWidth = max(
            minWidth,
            2 * calculateTextLength(label, textSize, True, 600) + 2*margin
        )
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
    for key in stats :
        label = stat_labels[key]
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
        lastUpdated, #11
        scholarLogoTemplate.format(margin, margin, scholarLogoDimensions),  #12
        scholarLogoTemplate.format(
            minWidth - margin - scholarLogoDimensions,
            margin,
            scholarLogoDimensions)  #13
    )
    return image.replace("\n", "")

def scrapePage(page) :
    """Scrapes some bibliometrics from the scholar profile page.

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
    metrics["total-cites"] = int(totalCitations.strip())
    i = endStat + 6
    endStat = page.find("</td>", i)
    if endStat < 0 :
        return metrics
    i += 5
    startStat = page.rfind(">", i, endStat)
    if startStat < 0 :
        return metrics
    fiveYearCitations = page[startStat+1:endStat]
    metrics["five-year-cites"] = int(fiveYearCitations.strip())
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
    metrics["h-index"] = int(h.strip())
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
    metrics["i10-index"] = int(i10.strip())
    return metrics
    
def parseBibliometrics(page, year) :
    """Parses a Scholar Profile for the bibliometrics.

    Keyword arguments:
    page - The user profile page
    year - The year of the first publication, which will be None if user
        didn't provide in the configuration (i.e., this is not scraped
        from profile)
    """
    calc = BibliometricCalculator(
        scrapePage(page),
        parse_cites_per_pub(page),
        year
    )
    metrics = calc.to_dict()
    validateMetrics(metrics)
    return metrics
    
def parse_cites_per_pub(page) :
    """Parses the cites per publication for calculating g-index,
    e-index, i100-index, etc.

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

def getConfiguration(configFilename) :
    """Gets the configuration file.

    Keyword arguments:
    configFilename - The configuration filename with path
    """
    if not os.path.isfile(configFilename) :
        print("Configuration file", configFilename, "not found.")
        exit(1)
    try :
        with open(configFilename, "r") as f :
            return json.load(f)
    except :
        print("Error while reading configuration file", configFilename)
        exit(1)

def outputJSON(filename, metrics) :
    """Outputs the bibliometrics to a json file.

    Keyword arguments:
    filename - The name of the json file with path.
    metrics - The dictionary of bibliometrics
    """
    # Create the directory if it doesn't exist.
    directoryName = os.path.dirname(filename)
    converted_metrics = {
        key : (
            float(value) if isinstance(value, str) else value
            ) for key, value in metrics.items()
    }
    if len(directoryName) > 0 :
        os.makedirs(directoryName, exist_ok=True, mode=0o777)
    try:
        # Write the metrics to a json file
        with open(filename, "w") as jsonFile :
            json.dump(converted_metrics, jsonFile, indent=4, sort_keys=True)
    except IOError:
        print("Error: An error occurred while writing the metrics to a json file.")
        exit(1)

def readPreviousBibliometrics(filename) :
    """Reads the previous bibliometrics from the json file
    if it exists. Returns None if it doesn't exist or otherwise cannot be read.

    Keyword arguments:
    filename - The filename of the json file with path from the prior run.
    """
    if os.path.isfile(filename) :
        try :
            with open(filename, "r") as f :
                return json.load(f)
        except :
            return None
    return None

def getScholarProfilePage(profileID) :
    """Gets the Scholar profile page.

    Keyword arguments:
    profileID - Scholar profile ID
    """
    url = urlTemplate.format(profileID)
    try :
        with urlopen(url) as response :
            return response.read().decode(response.headers.get_content_charset())
    except HTTPError as e:
        print("ERROR: Failed to retrieve the profile page!")
        print(e.status)
        print(e.reason)
        print(e.headers)
        print("Exiting....")
        exit(1)

def validateMetrics(metrics):
    """Checks for parsing errors.

    Keyword arguments:
    metrics - The parsed and computed bibliometrics
    """
    valid = True
    if "total-cites" not in metrics:
        valid = False
        print("ERROR: Failed to parse total citations.")
    if "five-year-cites" not in metrics:
        valid = False
        print("ERROR: Failed to parse five-year citations.")
    if "h-index" not in metrics:
        valid = False
        print("ERROR: Failed to parse h-index.")
    if "i10-index" not in metrics:
        valid = False
        print("ERROR: Failed to parse i10-index.")
    if "g-index" not in metrics :
        print("WARNING: Failed to parse data needed to compute g-index.")
    if "h-median" not in metrics:
        print("WARNING: Failed to parse data needed to compute h-median.")
    if "e-index" not in metrics:
        print("WARNING: Failed to parse data needed to compute e-index.")
    if "r-index" not in metrics:
        print("WARNING: Failed to parse data needed to compute R-index.")
    if "a-index" not in metrics:
        print("WARNING: Failed to parse data needed to compute A-index.")
    if "most-cited" not in metrics:
        print("WARNING: Failed to parse data needed to compute most-cited paper.")
    if "w-index" not in metrics:
        print("WARNING: Failed to parse data needed to compute w-index.")
    if "o-index" not in metrics:
        print("WARNING: Failed to parse data needed to compute o-index.")
    if not valid :
        print("Exiting....")
        exit(1)

def main() :
    """Entry point for the utility."""
    configuration = getConfiguration(".bibliometrics.config.json")

    previousMetrics = readPreviousBibliometrics(
        configuration["jsonOutputFile"]) if "jsonOutputFile" in configuration else None

    scholarID = os.environ["SCHOLAR_ID"] if "SCHOLAR_ID" in os.environ else None
    if scholarID == None :
        if "scholarID" in configuration :
            scholarID = configuration["scholarID"]

    if scholarID == None :
        print("No Scholar ID provided.")
        print("Set either via SCHOLAR_ID environment variable or scholarID field in config file.")
        print("Exiting....")
        exit(1)

    page = getScholarProfilePage(scholarID)

    metrics = parseBibliometrics(
        page,
        configuration["firstPubYear"] if "firstPubYear" in configuration else None
    )
    
    # default metrics in default order
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
        "w-index",
        "o-index",
        "h-median",
        "m-quotient",
        "e-index",
        "r-index",
        "a-index"
    ]

    # check if user-specified metrics order for all SVGs
    if "include" in configuration :
        stats = [ key.lower() for key in configuration["include"] ]

    if previousMetrics != metrics :
        if "jsonOutputFile" in configuration :
            outputJSON(configuration["jsonOutputFile"], metrics)
            
        for colors in configuration["svgConfig"] :
            stats_to_include = [
                key.lower() for key in colors["include"]
                ] if "include" in colors else stats
            image = generateBibliometricsImage(
                metrics,
                colors,
                "Bibliometrics",
                stats_to_include
            )
            outputImage(image, colors["filename"])
