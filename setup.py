from setuptools import setup

setup(
    name="nistpt",
    version="0.0.3",
    description="NIST database scraper",
    long_description=("NIST database scraper" "to get elements information"),
    author="lebdt",
    url="https://github.com/lebdt/nistpt",
    keywords=["NIST", "Periodic Table"],
    entry_points={"console_scripts": ["nistpt = nistpt.cli:main"]},
    install_requires=[
        "selenium",
        "tabulate >= 0.9.0",
    ],
    license="MIT License",
)
