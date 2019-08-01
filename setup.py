import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysite-django-pkg-cgrbyk",
    version="0.0.1",
    author="cgrbyk",
    author_email="cgrbyk@gmail.com",
    description="Django mysite package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cgrbyk/djangopolls",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)