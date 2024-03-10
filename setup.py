from setuptools import setup, find_packages

setup(
    name="cognos",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jax",
        "jupyter",
        "ipykernel",
        "openai",
        "numpy",
        "pandas",
        "typing",
        "pydantic",
        "httpx",
    ],
)
