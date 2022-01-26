
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wpyblog",
    version="0.0.1",
    author="Fathur Rahman",
    author_email="fathur@lalokalabs.co",
    description="Show wordpress blog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lalokalabs/wpyblog",
    project_urls={
        "Bug Tracker": "https://github.com/lalokalabs/wpyblog/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
