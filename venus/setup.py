
from setuptools import setup, find_packages

setup(
        name="venus",
        version="0.0a1",
        description="",
        author="UT IEEE RAS",
        # author_email="",
        packages=find_packages(),
        install_requires=[
            ],
        entry_points={
            'console_scripts': [
                "venus = venus.venus:main"
                ],
            },
        )
