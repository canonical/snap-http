from setuptools import setup

setup(
    name="test_snap",
    description="A test snap",
    license="GPL-2.0",
    python_requires=">=3.8",
    packages=["test_snap"],
    entry_points={
        "console_scripts": ["test-snap=test_snap.main:main"],
    },
)
