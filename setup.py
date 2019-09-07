from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='pynq_emulator',
    version='1.0',
    description="An emulator for TUNI students' PYNQ exercises",
    author='Riku Salminen',
    author_email='riku.salminen@tuni.fi',
    packages=['pynq_emulator'],  #same as name
    install_requires=[], #external packages as dependencies
    scripts=[],
    url="https://github.com/Riku-S/led-matrix",
    download_url="https://github.com/Riku-S/led-matrix/archive/master.zip"
)