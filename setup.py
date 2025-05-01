from setuptools import setup, find_packages

setup(
    name="lisq",
    version="0.1.0",
    description="Single file note-taking app that work with .txt files",
    author="funnut",
    author_email="twoj@email.com",
    packages=find_packages(),
    install_requires=[
        "requests",  # przykładowa zależność
    ],
    include_package_data=True,
    zip_safe=False
)
