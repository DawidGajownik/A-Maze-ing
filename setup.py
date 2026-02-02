from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    packages=find_packages(include=['mazegen', 'mazegen.*']),
    install_requires=[],
    description=("A maze generation library providing tools to generate and" +
                 " solve mazes."),
    author="skolsut",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
