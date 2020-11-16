from setuptools import setup

readme = ''

setup(
    long_description=readme,
    name='vip-ipykernel',
    version='0.1.0',
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
