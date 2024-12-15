from setuptools import setup, find_packages

setup(
    name="okx_quant",
    version="0.0.6",
    packages=find_packages(),
    author="openhe",
    author_email="hezhewen2004@gmail.com",
    description="okx quant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/openhe-hub/okx-quant',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
