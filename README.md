# Yandex Images Crawler

[![PyPI - Version](https://img.shields.io/pypi/v/yandex-images-crawler?style=for-the-badge&color=blue)](https://pypi.org/project/yandex-images-crawler/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/yandex-images-crawler?style=for-the-badge&color=mediumpurple)](https://www.pepy.tech/projects/yandex-images-crawler)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yandex-images-crawler?style=for-the-badge)](https://pypi.python.org/pypi/yandex-images-crawler)
[![GitHub License](https://img.shields.io/github/license/suborofu/yandex-images-crawler?style=for-the-badge&color=limegreen)](https://opensource.org/licenses/MIT)

## Description

`Yandex Images Crawler` allows you to download images from [Yandex Images](https://yandex.com/images) automatically.

Unlike most other projects, this package allows you to download images according to certain filters. For example, you can download images of a specified size or similar images.

## Installation

You can use the `yandex_images_crawler/download.py` script or install the package via `pip`

```
pip install yandex-images-crawler
```

## Usage

```
C:\Users\suborofu> yandex-images-crawler --help
usage: yandex-images-crawler [-h] [--links LINK1,...] [--links-file FILE] [--size WxH] [--count N]
                             [--dir DIR] [--prev-dir DIR]

Yandex Images Crawler

options:
  -h, --help         show this help message and exit
  --links LINK1,...  Full links to image sets for download. Links should be separated by commas. Each    
                     link should lead to an open preview of the image.
  --links-file FILE  Text file with full links to image sets for download. Links should be separated by  
                     newlines. Each link should lead to an open preview of the image.
  --size WxH         Minimum size of images to download. Width an height should be separated by 'x'.     
  --count N          Required count of images to download. A message appears if the desired number of    
                     images are downloaded.
  --dir DIR          Directory for new images.
  --prev-dir DIR     Directory of previously loaded images. Program skips the loading of already loaded  
                     images in another directory. Useful for re-downloading.
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
5. Copy a link in the browser ([example](https://yandex.com/images/search?img_url=https%3A%2F%2F1.bp.blogspot.com%2F-oVRA16EtMGI%2FYDFWXxU36AI%2FAAAAAAAGHLw%2FbdLd23pcZIoqDXZMrQZ-bWRsYan8hIm9wCLcBGAsYHQ%2Fs1600%2Frickroll4k.gif&lr=10831&pos=0&quality=95&rdrnd=174777&redircnt=1700337169.1&rpt=simage&sign=304c88d47ac4545285d022ba151a7c35&text=rick%20roll%20meme&type=album)).
