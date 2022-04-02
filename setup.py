from setuptools import setup, find_packages

setup(
    name='jsd-gen',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/badf00d21/JSD2021',
    license='MIT',
    package_data={'': ['./generator_app/*.tx', './generator_app/*.txt', './templates/**/*.j2', './templates/*.j2',
                       './static_files/*', './static_files/**/*', './static_files/**/**/*',
                       './static_files/**/**/**/*.properties', './static_files/**/**/**/*.jar', './model_meta_model/*', './model_meta_model/*.txt', './model_meta_model/*.tx']},
    include_package_data=True,
    author='badf00d21',
    author_email='jiricekova31@gmail.com',
    description='DSL for generating SpringBoot project. \n Petar Makevic E2/144-2019 ',
    entry_points={
        'console_scripts': [
            'jsd-gen=generator_app:call_generate'
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
        'Programming Language :: PyThon :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
)
