from setuptools import setup, find_packages

setup(
    name="lisq",
    version="2025.05.01",
    description="Single file note-taking app that work with .txt files",
    author="funnut",
    author_email="essdoem@yahoo.com",
    project_urls={
        "Bug Trucker": "https://github.com/funnut/Lisq/issues",
        "Source Code": "https://github.com/funnut/Lisq.git",
    },
    url="https://github.com/funnut/Lisq",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "lisq = lisq.lisq:main"
        ]
    },
    license="Non-Commercial",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
