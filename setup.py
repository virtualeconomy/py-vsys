import setuptools
import os

# read the contents of your README file
this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md")) as f:
    long_description = f.read()

setuptools.setup(
    name="py-v-sdk",
    version="0.1.0",
    description="The official Python SDK for VSYS APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "SDK",
        "api wrapper",
        "blockchain",
        "vsystems",
        "smart contract",
        "supernode",
        "defi",
    ],
    url="https://github.com/virtualeconomy/py-v-sdk",
    author="V SYSTEMS",
    author_email="developers@v.systems",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "aiohttp~=3.8.1",
        "python-axolotl-curve25519~=0.4.1.post2",
        "base58~=2.1.1",
        "loguru~=0.5.3",
    ],
    python_requires=">=3.9",
)
