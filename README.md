# Yandex Images Crawler

[![PyPI version](https://badge.fury.io/py/yandex-images-crawler.svg)](https://pypi.python.org/pypi?:action=display&name=yandex-images-crawler)
[![Downloads](https://pepy.tech/badge/yandex-images-crawler)](https://pepy.tech/project/yandex-images-crawler)
[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)

## Description

`Yandex Images Crawler` allows you to download images from [Yandex Images](https://yandex.com/images) automatically.

Unlike most other projects, this package allows you to download images according to certain filters. For example, you can download images of a specified size or similar images.

## Installation

You can use the `yandex_images_crawler/download.py` script or install the package via `pip`

```cmd
pip install yandex-images-crawler
```

## Usage

```cmd
C:\Users\suborofu> yandex-images-crawler --help
usage: yandex-images-crawler [-h] [--links LINK1,LINK2,...] [--links-file FILE] [--size WxH] [--count N] [--dir DIR]
                             [--prev-dir DIR]

Yandex Images Crawler

options:
  -h, --help            show this help message and exit
  --links LINK1,LINK2,...
                        Full links to image sets for download. Links should be separated by commas. Each link should
                        lead to an open preview of the image.
  --links-file FILE     Text file with full links to image sets for download. Links should be separated by newlines.
                        Each link should lead to an open preview of the image.
  --size WxH            Minimum size of images to download. Width an height should be separated by 'x'.
  --count N             Required count of images to download. A message appears if the desired number of images are
                        downloaded
  --dir DIR             Directory for new images.
  --prev-dir DIR        Directory of previously loaded images. Useful for skipping the loading of already separated
                        images in another directory.
```

### Links

To get correct links, follow the steps below:

1. Open [Yandex Images](https://yandex.com/images).
2. Search for images you need.
3. Set the search parameters:
   - Specify size, orientation, type or color.
   - Provide a site URL.
   - Find similar images.
4. Open the first image preview.
5. Copy a link in the browser.
