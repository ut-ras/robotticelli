
from setuptools import setup, find_packages

setup(
        name="primavera",
        version="0.0a1",
        description="",
        author="UT IEEE RAS",
        # author_email="",
        packages=find_packages(),
        install_requires=[
        ],
        entry_points={
            'console_scripts': [
                "primavera = primavera.primavera:main"
                ],
            },
        )
