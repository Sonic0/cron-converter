from setuptools import setup, find_packages

setup(
    name='cron-converter',
    version='0.0.1',
    license='MIT License',
    description='Cron string parser for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrea Salvatori',
    author_email='andrea.salvatori92@gmail.com',
    url='https://github.com/Sonic0/cron-converter',
    packages=find_packages('src', exclude=['tests*', '*.tests*']),
    keywords='cron',
    # install_requires=,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires='>=3.8',
)
