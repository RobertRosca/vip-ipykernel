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


setup(
    name='vip-ipykernel',
    url='https://github.com/RobertRosca/vip-ipykernel',
    descripton="IPython Kernel that loads a Virtualenv in a Parent Directory",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    version=get_version("./src/vip_ipykernel/__init__.py"),
    python_requires='==3.*,>=3.6.0',
    author='Robert Rosca',
    author_email='32569096+RobertRosca@users.noreply.github.com',
    py_modules=['vip_ipykernel_launcher'],
    packages=['vip_ipykernel'],
    package_dir={"": "src"},
    install_requires=[
        'jupyter-client>=4.2',
        'ipykernel>=4.4',
    ],
    extras_require={
        'test': [
            'pytest==5.*,>=5.2.0',
            'pytest-cov==2.*,>=2.10.1',
            'nose==1.*,>=1.3.7',
            'nbval==0.9.*,>=0.9.6',
        ],
    },
)
