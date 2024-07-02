from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="chess2postgres",
    author="lot022",
    version="0.0.2",
    license="MIT",
    keywords="chess",
    python_requires=">=3.7",
    url="https://github.com/lot022/chess2postgres",
    description="Simple python library to fetch games directly into Postgres database from Lichess.org using it's API or pgn file containing games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['berserk', 'psycopg2-binary', 'chessanalytics'],
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
