from setuptools import setup, find_packages

setup(
    name='VidETL',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "whisper-timestamped==1.14.2",
        "Pillow==9.4.0",
        "moviepy==1.0.3",
        "fastapi==0.109.0",

    ]
)
