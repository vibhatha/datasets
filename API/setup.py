#!/usr/bin/env python3
"""
Setup script for the opendata package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "opendata", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "A Python library for traversing folder structures with meta.yml files"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "opendata", "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ["PyYAML>=6.0"]

setup(
    name="opendata",
    version="1.0.0",
    description="A Python library for traversing folder structures with meta.yml files and understanding graph entities for database integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="OpenData Team",
    author_email="opendata@example.com",
    url="https://github.com/your-username/opendata",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "opendata=opendata.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="data traversal yaml graph entities database",
    project_urls={
        "Homepage": "https://github.com/your-username/opendata",
        "Documentation": "https://opendata.readthedocs.io",
        "Repository": "https://github.com/your-username/opendata",
        "Issues": "https://github.com/your-username/opendata/issues",
    },
)
