try:
    from .crawler import YandexCrawler
except ImportError:
    from crawler import YandexCrawler
from typing import List, Tuple, Union
from pathlib import Path
import time
import os
import logging
from multiprocessing import Process
import argparse


def __check_status(proc_num: int, image_dir: Union[str, Path], image_count: int):
    while True:
        time.sleep(60)
        now = time.time()
        for i in range(proc_num):
            if now - os.path.getmtime(Path(__file__).parent / f"temp{i}") > 120:
                logging.warn(f"Process #{i} does not download images. Please check it.")
        for _, _, files in os.walk(image_dir):
            if image_count != -1 and len(files) > image_count:
                logging.info(
                    "The required number of images is reached. You can stop executing the script."
                )
            break


def __start_crawler(link, image_size, image_dir, previous_images, id):
    crawler = YandexCrawler(
        link=link,
        image_size=image_size,
        image_dir=image_dir,
        previous_images=previous_images,
        id=id,
    )
    crawler.run()


def download(
    links: List[str],
    image_size: Tuple[int, int],
    image_count: int,
    image_dir: Union[str, Path],
    previous_images: List[Union[str, Path]],
):
    proc_num = len(links)
    processes = [
        Process(
            target=__start_crawler,
            args=(links[i], image_size, image_dir, previous_images, i),
        )
        for i in range(proc_num)
    ] + [Process(target=__check_status, args=(proc_num, image_dir, image_count))]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def __parse_args():
    parser = argparse.ArgumentParser(description="Yandex Images Crawler", add_help=True)
    parser.add_argument(
        "--links",
        type=str,
        metavar="LINK1,LINK2,...",
        default=None,
        required=False,
        help="""Full links to image sets for download.
        Links should be separated by commas.
        Each link should lead to an open preview of the image.""",
    )
    parser.add_argument(
        "--links-file",
        type=str,
        metavar="FILE",
        default=None,
        required=False,
        help="""Text file with full links to image sets for download.
        Links should be separated by newlines.
        Each link should lead to an open preview of the image.""",
    )
    parser.add_argument(
        "--size",
        type=str,
        metavar="WxH",
        default="0x0",
        required=False,
        help="""Minimum size of images to download.
        Width an height should be separated by 'x'.""",
    )
    parser.add_argument(
        "--count",
        type=int,
        metavar="N",
        default=-1,
        required=False,
        help="""Required count of images to download.
        A message appears if the desired number of images are downloaded""",
    )
    parser.add_argument(
        "--dir",
        type=str,
        metavar="DIR",
        default="yandex-images",
        required=False,
        help="Directory for new images.",
    )
    parser.add_argument(
        "--prev-dir",
        type=str,
        metavar="DIR",
        default=None,
        required=False,
        help="""Directory of previously loaded images.
        Useful for skipping the loading of already separated images in another directory.""",
    )

    args = parser.parse_args()
    new_args = argparse.Namespace()

    new_args.links = []
    if args.links is not None and args.links_file is not None:
        logging.critical("Provide links via --links only or --links_file only")
        exit(-1)
    if args.links is not None:
        new_args.links = args.links.split(",")
    if args.links_file is not None:
        with open(args.links_file, "r") as f:
            new_args.links = f.read().strip().split()
    if len(new_args.links) == 0:
        logging.critical("Provide links via --links only or --links_file only")
        exit(-1)

    new_args.size = tuple(map(int, args.size.split("x")))

    new_args.count = args.count

    new_args.image_dir = Path(args.dir)

    new_args.previous_images = []
    for _, _, files in os.walk(new_args.image_dir):
        new_args.previous_images.extend(files)
        break

    if args.prev_dir is not None:
        for _, _, files in os.walk(args.prev_dir):
            new_args.previous_images.extend(files)

    return new_args


def main():
    args = __parse_args()
    download(args.links, args.size, args.count, args.image_dir, args.previous_images)


if __name__ == "__main__":
    main()
