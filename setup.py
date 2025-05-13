from setuptools import setup, find_packages

setup(
    name='log-analyzer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'log-analyzer=log_analyzer.analyzer:main',
        ],
    },
    author='Mete',
    description='CLI Log Analiz Aracı',
    url='https://github.com/mete957/log-analyzer',
)
