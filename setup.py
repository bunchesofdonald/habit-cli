from setuptools import setup

setup(
    name="habit-cli",
    version="0.1",
    py_modules=["habbit"],
    install_requires=["click>=7.0", "pendulum", "python-jenkins", "terminaltables"],
    entry_points="""
        [console_scripts]
        hb=habit:cli
    """,
)
