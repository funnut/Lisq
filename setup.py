from setuptools import setup, find_packages

setup(
    name="lisq",
    version="0.11.1",
    description="Single file note-taking app that work with .txt files",
    author="funnut",
    author_email="",
    url="https://github.com/funnut/Lisq",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "lisq = lisq.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # zmień jeśli masz inny
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
