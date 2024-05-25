from setuptools import setup, find_packages

"""
This module, cognOS, uses PDM and pyproject.toml
- `lager` is a dependency and it uses setuptools
- `cognosis` is installed and handled at runtime (after REPL begins)
"""

setup(
    name="cognos",
    version="0.1.0",
    description="cognOS for cognosis, namespace and filesystem interface; obsidian kb",
    author="MOONLAPSED",
    author_email="MOONLAPSED@gmail.com",
    packages=find_packages(where='src'),
    install_requires=[
        "lager @ git+https://github.com/MOONLAPSED/lager.git@1.0.0",
    ],
    python_requires='>=3.11'
)
