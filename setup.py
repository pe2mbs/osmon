from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text( encoding = "utf-8" )


setup(
    name                            = "osmon",  # Required
    version                         = "1.0.0",
    description                     = "OSMON daemon to monitor processes",  # Optional
    long_description                = long_description,  # Optional
    long_description_content_type   = "text/markdown",  # Optional (see note above)
    url                             = "https://github.com/pe2mbs/osmon",  # Optional
    author                          = "Marc Bertens-Nguyen",
    author_email                    = "m,bertens@pe2mbs.nl",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)"
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords                        = "OSMON daemon process monitor",
    package_dir                     = { "": "src"},
    packages                        = find_packages( where = "src" ),
    python_requires                 = ">=3.7, <4",
    entry_points = {
        "console_scripts": [
            "osmon=osmon.__main__:startup",
            "oscom=oscom.__main__:main",
        ],
    },
    project_urls = {
        "Bug Reports": "https://github.com/pe2mbs/osmon/issues",
        "Source": "https://github.com/pe2mbs/osmon",
    },
)

