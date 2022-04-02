from setuptools import setup, find_packages

setup(
    name='jsd-gen-badf00d21',
    version='1.0.1',
    packages=find_packages(),
    url='https://github.com/badf00d21/JSD2021',
    license='MIT',
    package_data={'': ['./generator_app/*.tx', './generator_app/*.txt', './templates/**/*.j2', './templates/*.j2',
                       './static_files/*', './static_files/**/*', './static_files/**/**/*',
                       './static_files/**/**/**/*.properties', './static_files/**/**/**/*.jar', './model_meta_model/*', './model_meta_model/*.txt', './model_meta_model/*.tx']},
    include_package_data=True,
    author='badf00d21',
    author_email='jiricekova31@gmail.com',
    description='DSL for generating SpringBoot project.\n\nMade by: Petar Makevic E2/144-2019 \n',
    entry_points={
        'console_scripts': [
            'jsd-gen-badf00d21=generator_app:call_generate'
        ]
    },
    install_requires=['Jinja2', 'textX-dev'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
)
