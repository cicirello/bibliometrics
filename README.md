# bibliometrics

This command line utility does the following:
* retrieves the first page of your Google Scholar profile;
* parses from that page your total citations, your five-year citation count, your h-index, your i10-index, and the number of citations of your most-cited paper;
* computes your g-index provided if it is less than 100 ([reason for limitation later](#respect-google-scholars-robotstxt));
* generates a JSON file summarizing these bibliometrics; and
* generates one or more SVG images summarizing these bibliometrics.

## Table of Contents

This README is organized as follows:
* [Samples](#samples): provides examples of the output of this utility.
* [Configuration](#configuration): explains how to configure the utility, such as colors for the SVG,
  file locations, etc.
* [Configuring the Scholar ID](#configuring-the-scholar-id): explains the two ways of providing your
  Google Scholar ID to the utility.
* [Usage](#usage): how to install and run.
* [Respect Google Scholar's robots.txt](#respect-google-scholars-robotstxt): explains the relevant 
  portions of Google Scholar's robots.txt as it relates to this, or any tool, designed to gather information 
  from Scholar. Note that most other tools that provide more functionality (e.g., all of the ones I looked at before
  implementing this) do not respect that robots.txt. If you wish to submit an issue or pull request requesting 
  additional functionality, please know that any such request must be possible to implement without violating 
  Scholar's robots.txt. Otherwise, the issue or pull request will be closed.
* [License](#license).

## Samples

Here are a couple sample SVGs.

![Example 1](https://raw.githubusercontent.com/cicirello/bibliometrics/main/images/bibliometrics.svg)

![Example 2](https://raw.githubusercontent.com/cicirello/bibliometrics/main/images/bibliometrics2.svg)

Here is a sample of the JSON summary also generated by the utility:

```JSON
{
    "fiveYear": 376,
    "g": 45,
    "h": 25,
    "i10": 33,
    "most": 228,
    "total": 2064
}
```

The above sample is also found in this 
repository: [bibliometrics.json](https://github.com/cicirello/bibliometrics/blob/main/bibliometrics.json), 
and the sample SVGs are found in the [images](https://github.com/cicirello/bibliometrics/blob/main/images) directory.

## Configuration

The utility looks for a configuration file `.bibliometrics.config.json` in your current 
working directory (please note the `.` at the start of the filename). A sample is found
at the root of this repository: [.bibliometrics.config.json](https://github.com/cicirello/bibliometrics/blob/main/.bibliometrics.config.json).

To generate the JSON summary of your bibliometrics, specify the filename (optionally with path)
via the `"jsonOutputFile"` field. If this field is not present, then no JSON file will be generated.

The `"svgConfig"` field is an array of JSON objects, such that each object configures one SVG. Each
of the JSON objects in this array includes the following fields:
* `"filename"` is the filename (optionally with path) to the target svg file.
* `"background"` is the background color.
* `"border"` is the border color.
* `"title"` is the title color.
* `"text"` is the color of the rest of the text.

The colors can be defined in any format that is valid within an SVG. For example, you can specify
RGB, two hex digits for each color channel, with `#010409`; or RGB with one hex digit for each color 
channel, `#123`. You can also use SVG named colors, such as `white`, as well as RGBA such as
`rgba(56,139,253,0.4)`. If it is valid as a color in SVG, then it should work. The utility simply inserts
it for the relevant color within the SVG without validation.

Here is a sample `.bibliometrics.config.json`:

```JSON
{
    "jsonOutputFile": "bibliometrics.json",
    "svgConfig": [
        {
            "background": "#010409",
            "border": "rgba(56,139,253,0.4)",
            "filename": "images/bibliometrics2.svg",
            "text": "#c9d1d9",
            "title": "#58a6ff"
        },
        {
            "background": "#f6f8fa",
            "border": "rgba(84,174,255,0.4)",
            "filename": "images/bibliometrics.svg",
            "text": "#24292f",
            "title": "#0969da"
        }
    ]
}
```

## Configuring the Scholar ID

There are two ways to provide your Google Scholar ID to the utility:
* in the configuration file (see above section) via a field `"scholarID"` (not shown in the example in the
  repository); or
* via an environment variable `SCHOLAR_ID`.

## Usage

### Installing

To install from PyPi (Unix and MacOS):

```Shell
python3 -m pip install bibliometrics
```

To install from PyPI (Windows):

```Shell
py -m pip install bibliometrics
```

To upgrade to latest version from PyPi (Unix and MacOS):

```Shell
python3 -m pip install --upgrade bibliometrics
```

To upgrade to latest version from PyPI (Windows):

```Shell
py -m pip install --upgrade bibliometrics
```

### Running

To use this utility, first ensure that you configure it as specified above. Then execute the following (Unix and MacOS):

```Shell
python3 -m bibliometrics
```

Or on Windows:

```Shell
py -m bibliometrics
```

## Respect Google Scholar's robots.txt

If you use this utility, please respect Google Scholar's robots.txt. The reason that the
g-index is only computed by this utility if it is less than 100 derives from Scholar's
robots.txt. Here is the relevant excerpt:

```robots.txt
Allow: /citations?user=
Disallow: /citations?*cstart=
```

The first line above allows getting a user's profile page. But the second line
above disallows querying a specific starting reference. This means if you are respecting
Google Scholar's robots.txt then you are limited to the first page of the profile, which
can include up to 100 publications. Therefore, we can compute g-index as long as it is not
greater than 100. However, if we compute 100, we cannot be certain if it is correct or if
it is actually higher, so this utility excludes a g-index of 100 as well.

## License

The code in this repository is released under
the [MIT License](https://github.com/cicirello/bibliometrics/blob/main/LICENSE).
