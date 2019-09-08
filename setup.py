import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='pynq_emulator',
    version='1.13',
    author='Riku Salminen',
    author_email='riku.salminen@tuni.fi',
    description="An emulator for TUNI students' PYNQ exercises",
	long_description = long_description,
    packages=setuptools.find_packages(exclude=[]),
    package_data = {},
	keywords='pynq emulator',
    scripts=[],
    url="https://github.com/Riku-S/led-matrix",
    download_url="https://github.com/Riku-S/led-matrix/archive/master.tar.gz",
    install_requires=[],
    classifiers = ["Natural Language :: English",
				   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
				   ],
	entry_points="""
	# -*- Entry points: -*-
    """,
)