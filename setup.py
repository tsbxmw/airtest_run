import setuptools, os
from setuptools import setup
from airrun.utils.version import __version__

PACKAGE_NAME = "airrun"

requires = [
    'twine',
    'setuptools',
    'airtest'
]

with open('README.md', encoding='utf8') as f:
    long_description = f.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


package_extras = []
package_extras.extend(package_files('{}/cli'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/report'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/utils'.format(PACKAGE_NAME)))


setup(
    name = 'airrun',
    version = __version__,
    author = 'wei.meng',
    author_email = 'mengwei1101@hotmail.com',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/tsbxmw/airtest_run',
    packages = setuptools.find_packages(exclude=['testcases']),
    package_data = {"": package_extras},
    python_requires='>=3.6',
    install_requires=requires,
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)