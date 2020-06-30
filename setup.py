import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentio-prober-control-SentioProberDev",
    version="0.1.5",
    author="Ingo Berg",
    author_email="ingo.berg@atv-systems.de",
    description="MPI Sentio Prober Control - Python Bindings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.mpi-corporation.com/ast/engineering-probe-systems/mpi-sentio-software-suite/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.6',
)