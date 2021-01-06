from setuptools import setup, find_packages

setup(
    name='cron-converter',
    version='0.1.0',
    license='MIT License',
    description='Cron string parser for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrea Salvatori',
    author_email='andrea.salvatori92@gmail.com',
    url='https://github.com/Sonic0/cron-converter',
    package_dir={'': 'src'},
    packages=['cron_converter', 'cron_converter/sub_modules'],
    # packages=find_packages(where='cron_converter', exclude=['tests*', '*.tests*']),
    keywords='cron',
    # install_requires=, # No requires
    include_package_data=True,
    extras_require={
            'test': ['unittest'],
        },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)
