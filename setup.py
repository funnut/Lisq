from setuptools import setup, find_packages

setup(
    name="lisq",
    version="2025.05.01",
    description="Single file note-taking app that work with .txt files",
    url="https://github.com/funnut/Lisq.git"
    author="funnut",
    author_email="twoj@email.com",
    project_urls={
        "Bug Trucker": "https://github.com/funnut/Lisq/issues",
        "Source Code": "https://github.com/funnut/Lisq.git",
    },
    packages=find_packages(),
    install_requires=[
        "requests",  # przykładowa zależność
    ],
    include_package_data=True,
    zip_safe=False
)
