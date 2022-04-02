from setuptools import setup, find_packages
import os

setup(
    name='badf00d21-sprinboot-gen',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/badf00d21/JSD2021',
    license='MIT',
    package_data={'': ['*.tx', '*.txt', './templates/**/*.j2']},
    include_package_data=True,
    author='badf00d21',
    author_email='jiricekova31@gmail.com',
    description='DSL for generating SpringBoot project. \n Petar Makevic E2/144-2019 ',
    entry_points={
        'console_scripts': [
            'badf00d21-sprinboot-gen=generator_app:main'
        ]
    },
    install_requires=['Jinja2', 'textX-dev'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: DSL Tools',
        'License :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Pyhon :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
)
