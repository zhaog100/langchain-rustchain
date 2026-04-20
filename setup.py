"""Setup script for langchain-rustchain."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-rustchain",
    version="1.0.0",
    author="xiaomili",
    author_email="zhaog100@gmail.com",
    description="RustChain integration for LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhaog100/langchain-rustchain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain-core>=0.1.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "mypy"],
    },
)
