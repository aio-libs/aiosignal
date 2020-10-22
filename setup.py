import pathlib
import re
import sys

from setuptools import setup

if sys.version_info < (3, 6):
    raise RuntimeError("aiosignal 1.x requires Python 3.6+")


here = pathlib.Path(__file__).parent


txt = (here / 'aiosignal' / '__init__.py').read_text('utf-8')
try:
    version = re.findall(r"^__version__ = '([^']+)'\r?$",
                         txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')

install_requires = [
    'frozenlist>=1.1.0',
]


def read(f):
    return (here / f).read_text('utf-8').strip()


args = dict(
    name='aiosignal',
    version=version,
    description='aiosignal: a list of registered asynchronous callbacks',
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.rst'))),
    long_description_content_type="text/x-rst",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Framework :: AsyncIO',
    ],
    author='Nikolay Kim',
    author_email='fafhrd91@gmail.com',
    maintainer='Martijn Pieters <mj@zopatista.com>',
    maintainer_email='aio-libs@googlegroups.com',
    url='https://github.com/aio-libs/aiosignal',
    project_urls={
        'Chat: Gitter': 'https://gitter.im/aio-libs/Lobby',
        'CI: GitHub Actions':
            'https://github.com/aio-libs/aiosignal/actions',
        'Coverage: codecov': 'https://codecov.io/github/aio-libs/aiosignal',
        'Docs: RTD': 'https://docs.aiosignal.org',
        'GitHub: issues': 'https://github.com/aio-libs/aiosignal/issues',
        'GitHub: repo': 'https://github.com/aio-libs/aiosignal',
    },
    license='Apache 2',
    packages=['aiosignal'],
    python_requires='>=3.6',
    install_requires=install_requires,
    include_package_data=True,
)

setup(**args)
