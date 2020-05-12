import re
import os.path

from setuptools import setup, find_packages

with open(
    os.path.join(os.path.dirname(__file__), "src", "flake8_markupsafe", "__init__.py")
) as f:
    VERSION = re.match(r".*__version__ = \"(.*?)\"", f.read(), re.S).group(1)

setup(
    name="flake8-markupsafe",
    version=VERSION,
    description="Flake8 plugin to detect dangerous markup",
    author="Vladimir Magamedov",
    author_email="vladimir@magamedov.com",
    url="https://github.com/vmagamedov/flake8-markupsafe",
    license="BSD-3-Clause",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "flake8.extension": ["MS = flake8_markupsafe.plugin:MarkupSafePlugin"],
    },
)
