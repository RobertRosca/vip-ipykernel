from setuptools import setup
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


readme = ''

setup(
    long_description=readme,
    name='vip-ipykernel',
    version=get_version("./src/vip_ipykernel/__init__.py"),
    python_requires='==3.*,>=3.6.0',
    author='Robert Rosca',
    author_email='32569096+RobertRosca@users.noreply.github.com',
    packages=['vip_ipykernel'],
    package_dir={"": "src"},
    package_data={
        "": ["resources/*.*"],
    },
    install_requires=[
        'jupyter-client==6.*,>=6.1.7',
    ],
    extras_require={
        'test': [
            'pytest==5.*,>=5.2.0',
            'pytest-cov==2.*,>=2.10.1',
            'nose==1.*,>=1.3.7',
            'ipykernel==5.*,>=5.3.4'
        ],
    },
)
