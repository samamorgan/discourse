import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='discourse',
    version='0.1.2',
    author='Sam Morgan',
    author_email='sama4mail@gmail.com',
    description='A Python wrapper of the Discourse API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/samamorgan/discourse',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
    ],
    install_requires='requests',
)
