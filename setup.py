from setuptools import setup, find_packages

setup(
    name='flow-cli',
    version='1.0.0',
    description='A beautiful, minimalist Pomodoro & focus timer for the terminal.',
    author='Efe',
    packages=find_packages(),
    scripts=['flow.py'],
    install_requires=[
        'rich>=13.0.0'
    ],
    entry_points={
        'console_scripts': [
            'flow=flow:main',
        ],
    },
)
