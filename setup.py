from pathlib import Path
from setuptools import setup, find_packages

parent_dir = Path(__file__).resolve().parent

setup(
    name="prettymapp",
    version="0.0.1",
    author="Christoph Rieke",
    author_email="christoph.k.rieke@gmail.com",
    description="",
    long_description=parent_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/chrieke/prettymapp",
    license="MIT",
    packages=find_packages(exclude=("tests", "streamlit-prettymapp")),
    package_data={"": ["fonts/PermanentMarker-Regular.ttf"]},
    data_files=[
        ("", ["requirements.txt"]),
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=parent_dir.joinpath("requirements.txt")
    .read_text(encoding="utf-8")
    .splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
)
