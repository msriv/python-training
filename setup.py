from setuptools import setup, find_packages

setup(
    name="python-training",
    version="0.1.0",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mihir",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.3.5",
        "pandas>=2.3.3",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "etl = python_training.src.app:main",
        ]
    },
    include_package_data=True,
)
