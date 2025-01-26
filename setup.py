from setuptools import setup
from pathlib import Path

NAME = "yandex-images-crawler"
VERSION = "1.3.1"
DESCRIPTION = "Crawler/parser for Yandex Images"
URL = "https://github.com/suborofu/yandex-images-crawler"
EMAIL = "alexfromsuvorov@gmail.com"
AUTHOR = "suborofu"
REQUIRES_PYTHON = ">=3.7"
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Image Processing",
    "Topic :: Utilities",
]
here = Path(__file__).parent

with open(here / "README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = "\n" + file.read()

requirements_path = Path(__file__).parent.absolute() / "requirements.txt"

with open(requirements_path, "r") as file:
    REQUIREMENTS = list(map(lambda line: line.strip(), file.readlines()))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    classifiers=CLASSIFIERS,
    url=URL,
    packages=["yandex_images_crawler"],
    entry_points={
        "console_scripts": [
            "yandex-images-crawler = yandex_images_crawler:main",
        ],
    },
    install_requires=REQUIREMENTS,
)
