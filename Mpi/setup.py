import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpi-probe-station-control",
    version="0.1.0",
    author="Ingo Berg",
    author_email="ingo.berg@atv-systems.de",
    description="MPI probe station control package",
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
)