from setuptools import setup, find_packages

setup(
    name='cron-converter',
    version='1.0.1',
    license='MIT License',
    description='Cron string parser and scheduler for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrea Salvatori',
    author_email='andrea.salvatori92@gmail.com',
    url='https://github.com/Sonic0/cron-converter',
    packages=['cron_converter', 'cron_converter/sub_modules'],
    keywords='cron',
    install_requires=['python-dateutil'],
    include_package_data=True,
    extras_require={
            'test': ['unittest'],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)
