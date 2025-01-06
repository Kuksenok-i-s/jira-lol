from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='jira-lol',
    version='0.1',
    description='A tool for automating time tracking in Jira',
    author='Kuksenok-i-s',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'jira-lol=main:main',
        ],
    },
)
